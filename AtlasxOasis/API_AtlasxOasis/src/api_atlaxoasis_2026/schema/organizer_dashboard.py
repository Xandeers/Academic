from pydantic import BaseModel
from typing import (
    List,
    Optional
)
from pydantic.config import ConfigDict
from datetime import date
from decimal import Decimal


class ChartData(BaseModel):
    date: date
    nb_sold: int
    revenue: Decimal


class TopEvent(BaseModel):
    id_event: int
    name: str
    value: float


class DashboardStat(BaseModel):

    #intervalle 
    start_date: date
    end_date :date 

    active_events_count: int     
    yearly_events_count: int      
    potential_total_revenue: Decimal

    monthly_revenue: Decimal      
    monthly_events_count: int

    avg_participants: float

    most_profitable_event: Optional[TopEvent]
    most_liked_event: Optional[TopEvent]
    most_attended_event: Optional[TopEvent]

    daily_sales_chart: List[ChartData] 
    weekly_total_revenue: Decimal


