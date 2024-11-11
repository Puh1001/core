# control/sprinkler.py
import logging
from enum import Enum
import asyncio
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SprinklerState(Enum):
    OFF = "OFF"
    ON = "ON"

class Sprinkler:
    def __init__(self, sprinkler_id: str):
        self.sprinkler_id = sprinkler_id
        self.state = SprinklerState.OFF
        self.last_state_change = None
        self.min_run_time = 30  # Thời gian tối thiểu chạy (giây)
        self.min_off_time = 300  # Thời gian tối thiểu nghỉ (giây)
        
    async def turn_on(self) -> bool:
        """Bật vòi phun"""
        if self.state == SprinklerState.OFF:
            self.state = SprinklerState.ON
            self.last_state_change = asyncio.get_event_loop().time()
            logger.info(f"Sprinkler {self.sprinkler_id} turned ON")
            return True
        return False
            
    async def turn_off(self) -> bool:
        """Tắt vòi phun"""
        if self.state == SprinklerState.ON:
            self.state = SprinklerState.OFF
            self.last_state_change = asyncio.get_event_loop().time()
            logger.info(f"Sprinkler {self.sprinkler_id} turned OFF")
            return True
        return False
    
    def can_change_state(self) -> bool:
        """Kiểm tra xem có thể thay đổi trạng thái không"""
        if self.last_state_change is None:
            return True
            
        current_time = asyncio.get_event_loop().time()
        time_since_last_change = current_time - self.last_state_change
        
        if self.state == SprinklerState.ON:
            return time_since_last_change >= self.min_run_time
        else:
            return time_since_last_change >= self.min_off_time

class SprinklerController:
    def __init__(self):
        self.sprinklers: Dict[str, Sprinkler] = {}
        self.is_auto_mode = True
        
    def add_sprinkler(self, sprinkler_id: str) -> None:
        """Thêm vòi phun mới vào hệ thống"""
        self.sprinklers[sprinkler_id] = Sprinkler(sprinkler_id)
        logger.info(f"Added sprinkler {sprinkler_id} to controller")
        
    def get_sprinkler(self, sprinkler_id: str) -> Optional[Sprinkler]:
        """Lấy thông tin vòi phun theo ID"""
        return self.sprinklers.get(sprinkler_id)
        
    async def control_sprinklers(self, issues: dict) -> None:
        """
        Điều khiển vòi phun dựa trên các vấn đề phát hiện được
        """
        if not self.is_auto_mode:
            return
            
        for sprinkler in self.sprinklers.values():
            should_turn_on = False
            
            # Kiểm tra độ ẩm đất
            if "soil_moisture" in issues:
                current_value, (min_value, max_value) = issues["soil_moisture"]
                if current_value < min_value:
                    should_turn_on = True
                    
            # Kiểm tra nhiệt độ đất
            if "soil_temperature" in issues:
                current_value, (min_value, max_value) = issues["soil_temperature"]
                if current_value > max_value:
                    should_turn_on = True
                    
            if should_turn_on and sprinkler.can_change_state():
                await sprinkler.turn_on()
            elif not should_turn_on and sprinkler.can_change_state():
                await sprinkler.turn_off()
                
    def set_auto_mode(self, enabled: bool) -> None:
        """Bật/tắt chế độ tự động"""
        self.is_auto_mode = enabled
        logger.info(f"Auto mode {'enabled' if enabled else 'disabled'}")
        
    async def manual_control(self, sprinkler_id: str, turn_on: bool) -> bool:
        """Điều khiển thủ công vòi phun"""
        sprinkler = self.get_sprinkler(sprinkler_id)
        if not sprinkler:
            return False
            
        if turn_on:
            return await sprinkler.turn_on()
        else:
            return await sprinkler.turn_off()