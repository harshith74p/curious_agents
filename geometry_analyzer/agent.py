import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString
from dataclasses import asdict

try:
    import osmnx as ox
    OSMNX_AVAILABLE = True
except ImportError:
    OSMNX_AVAILABLE = False

# Import from shared libraries
import sys
sys.path.append('../')
from libs.common import (
    get_logger, redis_manager, 
    calculate_distance, Topics, RedisKeys,
    dataclass_to_dict
)

class GeometryAnalyzer:
    def __init__(self):
        self.logger = get_logger("geometry_analyzer")
        self.redis = redis_manager
        
        # Road network cache
        self.road_networks = {}
        self.segment_geometries = {}
        
        # Configure OSMnx
        if OSMNX_AVAILABLE:
            ox.config(use_cache=True, log_console=True)
            self.logger.info("OSMnx initialized successfully")
        else:
            self.logger.warning("OSMnx not available - using simplified geometry analysis")
    
    async def analyze_network_capacity(self, latitude: float, longitude: float, radius_m: float = 2000) -> Dict:
        """Analyze road network capacity around a location"""
        self.logger.info(f"Analyzing network capacity for {latitude}, {longitude}")
        
        try:
            # Get or create road network
            network = await self._get_road_network(latitude, longitude, radius_m)
            
            if not network:
                return {"error": "Could not retrieve road network"}
            
            # Analyze network properties
            analysis = {
                "location": {"latitude": latitude, "longitude": longitude},
                "radius_m": radius_m,
                "network_stats": await self._calculate_network_stats(network),
                "capacity_analysis": await self._analyze_capacity(network),
                "bottlenecks": await self._identify_bottlenecks(network),
                "alternative_routes": await self._find_alternative_routes(network, latitude, longitude),
                "timestamp": datetime.now().isoformat()
            }
            
            # Cache the analysis
            await self._cache_analysis(latitude, longitude, analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing network capacity: {e}")
            return {"error": str(e)}
    
    async def find_optimal_routes(self, origin_lat: float, origin_lon: float, 
                                dest_lat: float, dest_lon: float, 
                                avoid_segments: List[str] = None) -> Dict:
        """Find optimal routes between two points, optionally avoiding congested segments"""
        self.logger.info(f"Finding routes from {origin_lat},{origin_lon} to {dest_lat},{dest_lon}")
        
        try:
            # Get road network that covers both points
            center_lat = (origin_lat + dest_lat) / 2
            center_lon = (origin_lon + dest_lon) / 2
            distance = calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
            radius_m = max(2000, distance * 1000 * 1.5)  # Ensure network covers route
            
            network = await self._get_road_network(center_lat, center_lon, radius_m)
            
            if not network:
                return {"error": "Could not retrieve road network"}
            
            # Find routes
            routes = await self._calculate_routes(network, origin_lat, origin_lon, 
                                                dest_lat, dest_lon, avoid_segments)
            
            return {
                "origin": {"latitude": origin_lat, "longitude": origin_lon},
                "destination": {"latitude": dest_lat, "longitude": dest_lon},
                "routes": routes,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error finding optimal routes: {e}")
            return {"error": str(e)}
    
    async def _get_road_network(self, latitude: float, longitude: float, radius_m: float) -> Optional[nx.MultiDiGraph]:
        """Get or create road network for a location"""
        cache_key = f"network_{latitude:.4f}_{longitude:.4f}_{int(radius_m)}"
        
        # Check if network is already cached
        if cache_key in self.road_networks:
            return self.road_networks[cache_key]
        
        try:
            if OSMNX_AVAILABLE:
                # Download road network from OpenStreetMap
                self.logger.info(f"Downloading road network for {latitude}, {longitude}")
                
                # Get network within radius
                G = ox.graph_from_point(
                    (latitude, longitude), 
                    dist=radius_m, 
                    network_type='drive',
                    simplify=True
                )
                
                # Add edge speeds and travel times
                G = ox.add_edge_speeds(G)
                G = ox.add_edge_travel_times(G)
                
                # Cache the network
                self.road_networks[cache_key] = G
                
                self.logger.info(f"Network loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
                return G
            else:
                # Create simplified mock network for demonstration
                return await self._create_mock_network(latitude, longitude, radius_m)
                
        except Exception as e:
            self.logger.error(f"Error getting road network: {e}")
            return None
    
    async def _create_mock_network(self, latitude: float, longitude: float, radius_m: float) -> nx.MultiDiGraph:
        """Create a simplified mock road network for testing"""
        G = nx.MultiDiGraph()
        
        # Create a simple grid network
        grid_size = 5
        spacing = 0.005  # Roughly 500m
        
        nodes = []
        for i in range(grid_size):
            for j in range(grid_size):
                lat = latitude + (i - grid_size//2) * spacing
                lon = longitude + (j - grid_size//2) * spacing
                node_id = i * grid_size + j
                G.add_node(node_id, y=lat, x=lon)
                nodes.append((node_id, lat, lon))
        
        # Add edges (roads)
        for i in range(grid_size):
            for j in range(grid_size):
                node_id = i * grid_size + j
                
                # Horizontal edges
                if j < grid_size - 1:
                    next_node = i * grid_size + (j + 1)
                    G.add_edge(node_id, next_node, length=500, speed_kph=50, travel_time=36)
                    G.add_edge(next_node, node_id, length=500, speed_kph=50, travel_time=36)
                
                # Vertical edges
                if i < grid_size - 1:
                    next_node = (i + 1) * grid_size + j
                    G.add_edge(node_id, next_node, length=500, speed_kph=50, travel_time=36)
                    G.add_edge(next_node, node_id, length=500, speed_kph=50, travel_time=36)
        
        return G
    
    async def _calculate_network_stats(self, network: nx.MultiDiGraph) -> Dict:
        """Calculate basic network statistics"""
        stats = {
            "total_nodes": network.number_of_nodes(),
            "total_edges": network.number_of_edges(),
            "total_length_km": 0,
            "average_degree": 0,
            "density": 0,
            "connectivity": 0
        }
        
        try:
            # Calculate total length
            total_length = sum(edge_data.get('length', 0) for _, _, edge_data in network.edges(data=True))
            stats["total_length_km"] = total_length / 1000
            
            # Average degree
            degrees = [network.degree(node) for node in network.nodes()]
            stats["average_degree"] = np.mean(degrees) if degrees else 0
            
            # Network density
            n = network.number_of_nodes()
            if n > 1:
                max_edges = n * (n - 1)
                stats["density"] = network.number_of_edges() / max_edges
            
            # Connectivity (simplified)
            stats["connectivity"] = nx.is_connected(network.to_undirected()) if n > 0 else False
            
        except Exception as e:
            self.logger.error(f"Error calculating network stats: {e}")
        
        return stats
    
    async def _analyze_capacity(self, network: nx.MultiDiGraph) -> Dict:
        """Analyze road capacity and flow characteristics"""
        capacity_analysis = {
            "high_capacity_roads": [],
            "low_capacity_roads": [],
            "capacity_distribution": {},
            "flow_analysis": {}
        }
        
        try:
            # Analyze each edge
            capacities = []
            for u, v, edge_data in network.edges(data=True):
                # Estimate capacity based on road attributes
                speed = edge_data.get('speed_kph', 50)
                length = edge_data.get('length', 500)
                
                # Simple capacity estimation (vehicles per hour)
                # This would be more sophisticated in a real system
                estimated_capacity = (speed / 50) * 2000  # Base capacity of 2000 veh/hr
                
                capacities.append(estimated_capacity)
                
                edge_info = {
                    "edge": f"{u}-{v}",
                    "length_m": length,
                    "speed_kph": speed,
                    "estimated_capacity": estimated_capacity
                }
                
                if estimated_capacity > 3000:
                    capacity_analysis["high_capacity_roads"].append(edge_info)
                elif estimated_capacity < 1000:
                    capacity_analysis["low_capacity_roads"].append(edge_info)
            
            # Capacity distribution
            if capacities:
                capacity_analysis["capacity_distribution"] = {
                    "mean": np.mean(capacities),
                    "median": np.median(capacities),
                    "std": np.std(capacities),
                    "min": np.min(capacities),
                    "max": np.max(capacities)
                }
            
        except Exception as e:
            self.logger.error(f"Error analyzing capacity: {e}")
        
        return capacity_analysis
    
    async def _identify_bottlenecks(self, network: nx.MultiDiGraph) -> List[Dict]:
        """Identify potential bottlenecks in the network"""
        bottlenecks = []
        
        try:
            # Calculate betweenness centrality to find critical nodes/edges
            node_centrality = nx.betweenness_centrality(network, weight='travel_time')
            edge_centrality = nx.edge_betweenness_centrality(network, weight='travel_time')
            
            # Find high centrality nodes (potential bottlenecks)
            high_centrality_threshold = np.percentile(list(node_centrality.values()), 90)
            
            for node, centrality in node_centrality.items():
                if centrality > high_centrality_threshold:
                    node_data = network.nodes[node]
                    bottlenecks.append({
                        "type": "node",
                        "id": str(node),
                        "latitude": node_data.get('y', 0),
                        "longitude": node_data.get('x', 0),
                        "centrality_score": centrality,
                        "degree": network.degree(node),
                        "description": f"High-traffic intersection (centrality: {centrality:.3f})"
                    })
            
            # Find high centrality edges
            edge_centrality_threshold = np.percentile(list(edge_centrality.values()), 90)
            
            for (u, v), centrality in edge_centrality.items():
                if centrality > edge_centrality_threshold:
                    edge_data = network.edges[u, v, 0]  # Get first edge if multiple
                    bottlenecks.append({
                        "type": "edge",
                        "id": f"{u}-{v}",
                        "centrality_score": centrality,
                        "length_m": edge_data.get('length', 0),
                        "speed_kph": edge_data.get('speed_kph', 50),
                        "description": f"Critical road segment (centrality: {centrality:.3f})"
                    })
            
        except Exception as e:
            self.logger.error(f"Error identifying bottlenecks: {e}")
        
        # Sort by centrality score
        bottlenecks.sort(key=lambda x: x['centrality_score'], reverse=True)
        return bottlenecks[:10]  # Return top 10
    
    async def _find_alternative_routes(self, network: nx.MultiDiGraph, center_lat: float, center_lon: float) -> List[Dict]:
        """Find alternative routes in the network"""
        alternatives = []
        
        try:
            # Find some sample origin-destination pairs
            nodes = list(network.nodes(data=True))
            if len(nodes) < 4:
                return alternatives
            
            # Sample a few node pairs for route analysis
            sample_pairs = [
                (nodes[0][0], nodes[-1][0]),  # Corners
                (nodes[len(nodes)//4][0], nodes[3*len(nodes)//4][0]),  # Middle sections
            ]
            
            for origin, destination in sample_pairs[:2]:  # Limit to avoid long computation
                try:
                    # Find shortest path
                    shortest_path = nx.shortest_path(
                        network, origin, destination, weight='travel_time'
                    )
                    shortest_time = nx.shortest_path_length(
                        network, origin, destination, weight='travel_time'
                    )
                    
                    # Find alternative path (remove one edge from shortest path)
                    if len(shortest_path) > 2:
                        # Temporarily remove an edge
                        u, v = shortest_path[len(shortest_path)//2], shortest_path[len(shortest_path)//2 + 1]
                        if network.has_edge(u, v):
                            network.remove_edge(u, v)
                            
                            try:
                                alt_path = nx.shortest_path(
                                    network, origin, destination, weight='travel_time'
                                )
                                alt_time = nx.shortest_path_length(
                                    network, origin, destination, weight='travel_time'
                                )
                                
                                alternatives.append({
                                    "origin_node": str(origin),
                                    "destination_node": str(destination),
                                    "primary_route": {
                                        "path": [str(n) for n in shortest_path],
                                        "travel_time": shortest_time
                                    },
                                    "alternative_route": {
                                        "path": [str(n) for n in alt_path],
                                        "travel_time": alt_time
                                    },
                                    "time_difference": alt_time - shortest_time
                                })
                                
                            except nx.NetworkXNoPath:
                                pass
                            
                            # Restore the edge
                            edge_data = network.edges.get((v, u), {})  # Get reverse edge data
                            network.add_edge(u, v, **edge_data)
                            
                except nx.NetworkXNoPath:
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error finding alternative routes: {e}")
        
        return alternatives
    
    async def _calculate_routes(self, network: nx.MultiDiGraph, origin_lat: float, origin_lon: float,
                              dest_lat: float, dest_lon: float, avoid_segments: List[str] = None) -> List[Dict]:
        """Calculate optimal routes between two geographic points"""
        routes = []
        
        try:
            # Find nearest nodes to origin and destination
            origin_node = await self._find_nearest_node(network, origin_lat, origin_lon)
            dest_node = await self._find_nearest_node(network, dest_lat, dest_lon)
            
            if origin_node is None or dest_node is None:
                return routes
            
            # Calculate primary route
            try:
                primary_path = nx.shortest_path(network, origin_node, dest_node, weight='travel_time')
                primary_time = nx.shortest_path_length(network, origin_node, dest_node, weight='travel_time')
                primary_distance = sum(
                    network.edges[primary_path[i], primary_path[i+1], 0].get('length', 0)
                    for i in range(len(primary_path)-1)
                )
                
                routes.append({
                    "route_type": "fastest",
                    "path_nodes": [str(n) for n in primary_path],
                    "travel_time_seconds": primary_time,
                    "distance_meters": primary_distance,
                    "coordinates": await self._get_route_coordinates(network, primary_path)
                })
                
            except nx.NetworkXNoPath:
                self.logger.warning("No path found between origin and destination")
            
            # Calculate alternative routes if avoiding segments
            if avoid_segments:
                modified_network = network.copy()
                # Remove edges corresponding to congested segments
                # This is simplified - in reality would need segment-to-edge mapping
                
                try:
                    alt_path = nx.shortest_path(modified_network, origin_node, dest_node, weight='travel_time')
                    alt_time = nx.shortest_path_length(modified_network, origin_node, dest_node, weight='travel_time')
                    alt_distance = sum(
                        modified_network.edges[alt_path[i], alt_path[i+1], 0].get('length', 0)
                        for i in range(len(alt_path)-1)
                    )
                    
                    routes.append({
                        "route_type": "avoiding_congestion",
                        "path_nodes": [str(n) for n in alt_path],
                        "travel_time_seconds": alt_time,
                        "distance_meters": alt_distance,
                        "coordinates": await self._get_route_coordinates(modified_network, alt_path)
                    })
                    
                except nx.NetworkXNoPath:
                    pass
            
        except Exception as e:
            self.logger.error(f"Error calculating routes: {e}")
        
        return routes
    
    async def _find_nearest_node(self, network: nx.MultiDiGraph, latitude: float, longitude: float) -> Optional[str]:
        """Find the nearest network node to a geographic point"""
        min_distance = float('inf')
        nearest_node = None
        
        for node, data in network.nodes(data=True):
            node_lat = data.get('y', 0)
            node_lon = data.get('x', 0)
            
            distance = calculate_distance(latitude, longitude, node_lat, node_lon)
            
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        
        return nearest_node
    
    async def _get_route_coordinates(self, network: nx.MultiDiGraph, path: List) -> List[List[float]]:
        """Get coordinate sequence for a route path"""
        coordinates = []
        
        for node in path:
            if node in network.nodes:
                node_data = network.nodes[node]
                lat = node_data.get('y', 0)
                lon = node_data.get('x', 0)
                coordinates.append([lon, lat])  # GeoJSON format: [lng, lat]
        
        return coordinates
    
    async def _cache_analysis(self, latitude: float, longitude: float, analysis: Dict):
        """Cache geometry analysis results"""
        cache_key = f"geometry_analysis:{latitude:.4f}:{longitude:.4f}"
        self.redis.set_with_expiry(cache_key, analysis, 3600)  # 1 hour cache
    
    async def get_segment_geometry(self, segment_id: str) -> Optional[Dict]:
        """Get geometric properties of a traffic segment"""
        # This would typically integrate with the traffic management system's segment definitions
        # For now, return mock geometry data
        
        mock_geometries = {
            "SEG001": {
                "segment_id": "SEG001",
                "start_point": {"latitude": 37.7749, "longitude": -122.4194},
                "end_point": {"latitude": 37.7759, "longitude": -122.4184},
                "length_meters": 1200,
                "lanes": 4,
                "speed_limit": 65,
                "road_type": "highway"
            }
        }
        
        return mock_geometries.get(segment_id) 