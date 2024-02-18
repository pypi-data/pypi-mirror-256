import json
from typing import Dict, List, Union

from pydantic import BaseModel


class Trade(BaseModel):
    """
    Represents a single trade.

    Attributes:
        price (float): Price of the trade
        volume (float): Volume of the trade
        timestamp (datetime): Timestamp of the trade
    """

    product_id: str
    price: float
    volume: float
    timestamp: int # in milliseconds

    def to_str(self) -> str:
        """
        Returns a string representation of the Trade object.
        """
        return json.dumps(self.model_dump())

    def to_dict(self) -> Dict[str, any]:
        """
        Convert the Trade object to a dictionary.

        Returns:
            dict: A dictionary representation of the Trade object.
        """
        return {
            "product_id": self.product_id,
            "price": self.price,
            "volume": self.volume,
            "timestamp": self.timestamp,
            # "Timestamp": self.timestamp, # required by Quix
        }
    
    # # a class method that can be used to create a Trade object from a list of values
    # @classmethod
    # def from_historical_kraken_api(
    #     cls,
    #     product_id: str,
    #     trade: List[Union[float, str]]
    # ) -> 'Trade':
    #     """
    #     Creates a Trade object from a list of values.

    #     Args:
    #         trade (List[Union[float, str]]): A list of values representing a trade.

    #     Returns:
    #         Trade: A Trade object.
    #     """
    #     breakpoint()
    #     return cls(
    #         product_id=product_id,
    #         price=float(trade[0]),
    #         volume=float(trade[1]),
    #         timestamp=int(float(trade[2]) * 1000), # milliseconds
    #     )
