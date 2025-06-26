from agents.base_agent import BaseAgent
from models.base import AIResponse, ServiceType
from services.navigation_service import NavigationService
from typing import List, Dict, Any
import json

class NavigationAgent(BaseAgent):
    """校园导航AI Agent"""
    
    def __init__(self):
        super().__init__()
        self.navigation_service = NavigationService()
    
    def get_service_type(self) -> ServiceType:
        return ServiceType.NAVIGATION
    
    def get_system_prompt(self) -> str:
        return """你是一个专业的校园导航助手，专门帮助学生找到校园内的各种地点和设施。

你的主要职责包括：
1. 地点查询和定位
2. 路线规划和导航
3. 校园地图服务
4. 设施信息查询
5. 交通指引

请提供准确、详细的导航信息，包括具体的位置描述和到达方式。"""
    
    def process_response(self, response: str) -> AIResponse:
        # 尝试从响应中提取地点信息
        locations = self.navigation_service.search_locations_by_keywords(response)
        
        metadata = {
            "locations": [location.dict() for location in locations[:5]] if locations else [],
            "total_locations": len(locations) if locations else 0
        }
        
        suggestions = [
            "查找教学楼",
            "查找图书馆",
            "查找食堂",
            "查找宿舍",
            "规划路线"
        ]
        
        return AIResponse(
            content=response,
            service_type=self.get_service_type(),
            confidence=0.90,
            metadata=metadata,
            suggestions=suggestions
        )
    
    async def find_location(self, location_name: str) -> AIResponse:
        """查找特定地点"""
        try:
            locations = self.navigation_service.search_locations_by_keywords(location_name)
            
            if locations:
                location = locations[0]
                prompt = f"""
                你是一个校园导航助手。
                你的任务是根据我提供的精确数据，为用户提供地点信息和导航。
                **你必须且只能使用下面 "=====" 分隔符内的数据来回答，严禁使用任何外部知识或自己数据库里的信息。**

                =====
                地点名称: {location.name}
                类别: {location.category}
                描述: {location.description}
                地址: {location.address}
                开放时间: {location.opening_hours or '根据校内规定'}
                坐标: {location.coordinates or '未提供'}
                =====

                请根据以上信息，为用户生成一份清晰的导航指南，包括：
                1.  **位置**: 清晰描述 "{location.name}" 的位置，可以参考它的类别和地址。
                2.  **周边参照**: 根据它的描述，告诉用户它附近可能有什么。
                3.  **导航建议**: 提供一些通用的校园内导航建议（如步行、骑行）。如果信息不足以提供详细路线，就这样说明。
                """
                
                response = await self.generate_response(prompt)
                response.metadata = {"location": location.dict()}
                
            else:
                response = AIResponse(
                    content=f'抱歉，没有在校园里找到与"{location_name}"相关的地点。请检查名称是否正确。',
                    service_type=self.get_service_type(),
                    confidence=0.0
                )
            
            return response
            
        except Exception as e:
            self.logger.error(f"查找地点时出错: {str(e)}")
            return AIResponse(
                content="抱歉，查找地点时出现错误，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def plan_route(self, start_location: str, end_location: str) -> AIResponse:
        """规划路线"""
        try:
            start_loc = self.navigation_service.get_location_by_name(start_location)
            end_loc = self.navigation_service.get_location_by_name(end_location)
            
            if not start_loc or not end_loc:
                return AIResponse(
                    content="抱歉，无法找到指定的起点或终点，请检查地点名称。",
                    service_type=self.get_service_type(),
                    confidence=0.0
                )
            
            # 获取路线信息
            route_info = self.navigation_service.get_route(start_loc, end_loc)
            
            prompt = f"""
            请为学生规划从{start_location}到{end_location}的路线：
            
            起点：{start_loc.name} ({start_loc.address})
            终点：{end_loc.name} ({end_loc.address})
            
            路线信息：{route_info}
            
            请提供：
            1. 详细的步行路线
            2. 预计时间
            3. 沿途的重要地标
            4. 注意事项
            """
            
            response = await self.generate_response(prompt)
            response.metadata = {
                "route": route_info,
                "start_location": start_loc.dict(),
                "end_location": end_loc.dict()
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"规划路线时出错: {str(e)}")
            return AIResponse(
                content="抱歉，规划路线时出现错误，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            )
    
    async def get_nearby_facilities(self, location_name: str, facility_type: str = None) -> AIResponse:
        """获取附近设施"""
        try:
            location = self.navigation_service.get_location_by_name(location_name)
            
            if not location:
                return AIResponse(
                    content=f"抱歉，没有找到名为'{location_name}'的地点。",
                    service_type=self.get_service_type(),
                    confidence=0.0
                )
            
            nearby_facilities = self.navigation_service.get_nearby_facilities(location, facility_type)
            
            prompt = f"""
            请介绍{location_name}附近的{facility_type or '设施'}：
            
            附近设施：{', '.join([f.name for f in nearby_facilities])}
            
            请提供：
            1. 每个设施的具体位置
            2. 距离和步行时间
            3. 设施的主要功能
            4. 使用建议
            """
            
            response = await self.generate_response(prompt)
            response.metadata = {
                "nearby_facilities": [facility.dict() for facility in nearby_facilities],
                "center_location": location.dict()
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"获取附近设施时出错: {str(e)}")
            return AIResponse(
                content="抱歉，获取附近设施时出现错误，请稍后再试。",
                service_type=self.get_service_type(),
                confidence=0.0
            ) 