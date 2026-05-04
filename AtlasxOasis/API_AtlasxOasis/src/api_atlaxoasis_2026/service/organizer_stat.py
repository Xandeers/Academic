from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import date, timedelta
from model import EventDB, TicketTypeEventDB, TicketDB, LikeDB, SaleObjectDB, PaymentDB
from typing import List, Dict
from schema.organizer_dashboard import DashboardStat, TopEvent


def get_general_value(db: Session, id_organizer: int):

    """Calcule les indicateurs globaux de l'organisateur."""
    
    today = date.today()
    curr_year = today.year

    #event actif( publié + à venir )
    activ_event = db.query(func.count(EventDB.id_event)).filter(
        and_(EventDB.id_organizer == id_organizer, EventDB.event_status == "published")
    ).scalar() or 0


    #event sur l'année 
    year_event= db.query(func.count(EventDB.id_event)).filter(
        and_(
            EventDB.id_organizer == id_organizer, 
            extract('year', EventDB.start_date) == curr_year
        )
    
    ).scalar() or 0


    potential_rev = db.query(func.sum(TicketTypeEventDB.price)).join(
        TicketDB, TicketDB.id_ticket_type == TicketTypeEventDB.id_ticket_type
    ).join(
        EventDB, EventDB.id_event == TicketTypeEventDB.id_event
    ).filter(
        and_(EventDB.id_organizer == id_organizer, EventDB.start_date >= today)
    ).scalar() or 0
    
    return {
        "active_events": activ_event,
        "yearly_events": year_event,
        "potential_revenue": potential_rev
    }
    

def get_monthly_stats(db: Session, id_organizer: int):
    """Calcule les stats sur le mois glissant (30 derniers jours)."""
    one_month_ago = date.today() - timedelta(days=30)
    
    # CA sur 1 mois et nombre d'events
    stats = db.query(
        func.count(func.distinct(EventDB.id_event)).label("nb_events"),
        func.sum(TicketTypeEventDB.price).label("revenue")
    ).join(TicketTypeEventDB, EventDB.id_event == TicketTypeEventDB.id_event
    ).join(TicketDB, TicketDB.id_ticket_type == TicketTypeEventDB.id_ticket_type
    ).filter(
        and_(EventDB.id_organizer == id_organizer, EventDB.start_date >= one_month_ago)
    ).first()

    return {
        "monthly_events": stats.nb_events or 0,
        "monthly_revenue": stats.revenue or 0
    }

def get_top_events(db: Session, id_organizer: int):
    """Récupère les événements records ."""
    
    # Plus lucratif
    top_revenue = db.query(
        EventDB.id_event, EventDB.name, func.sum(TicketTypeEventDB.price).label("val")
    ).join(TicketTypeEventDB).join(TicketDB).filter(EventDB.id_organizer == id_organizer
    ).group_by(EventDB.id_event).order_by(func.sum(TicketTypeEventDB.price).desc()).first()

    # Plus liké
    top_likes = db.query(
        EventDB.id_event, EventDB.name, func.count(LikeDB.id_customer).label("val")
    ).join(LikeDB).filter(EventDB.id_organizer == id_organizer
    ).group_by(EventDB.id_event).order_by(func.count(LikeDB.id_customer).desc()).first()

    return {
        "most_profitable": top_revenue,
        "most_liked": top_likes
    }



def get_daily_sales_chart(db: Session, id_organizer: int):
    """Génère les données pour le graphique des 7 derniers jours."""
    stats_list = []
    for i in range(6, -1, -1):
        target_date = date.today() - timedelta(days=i)
        
        # On compte les tickets créés à cette date précise
        data = db.query(
            func.count(TicketDB.id_ticket).label("count"),
            func.sum(TicketTypeEventDB.price).label("revenue")
        ).join(TicketTypeEventDB) \
         .join(EventDB) \
         .join(PaymentDB, TicketDB.id_payment == PaymentDB.id_payment) \
         .filter(
            and_(
                EventDB.id_organizer == id_organizer,
                func.date(PaymentDB.date_payment) == target_date
            )
        ).first()

        stats_list.append({
            "date": target_date,
            "nb_sold": data.count or 0,
            "revenue": data.revenue or 0
        })
    return stats_list

def get_most_attended_event(db:Session, id_organizer:int ):
    """Genere le nombre de participant moyen de l'organizer"""

    most_attended = db.query(
        EventDB.id_event, 
        EventDB.name, 
        func.count(TicketDB.id_ticket).label("val")
    ).join(TicketTypeEventDB, EventDB.id_event == TicketTypeEventDB.id_event) \
     .join(TicketDB, TicketDB.id_ticket_type == TicketTypeEventDB.id_ticket_type) \
     .filter(EventDB.id_organizer == id_organizer) \
     .group_by(EventDB.id_event) \
     .order_by(func.count(TicketDB.id_ticket).desc()) \
     .first()
    
    return{"most_attended": most_attended}



def get_avg_participant(db : Session, id_organizer:int):
    """Genere le nombre de participant moyen d'un organizer"""

    avg_participant=db.query(func.count(TicketDB.id_ticket).label("ticket_count")
    ).join(TicketTypeEventDB, TicketTypeEventDB.id_ticket_type == TicketDB.id_ticket_type) \
     .join(EventDB, EventDB.id_event == TicketTypeEventDB.id_event) \
     .filter(EventDB.id_organizer == id_organizer) \
     .group_by(EventDB.id_event) \
     .subquery()
    
    result = db.query(func.round(func.avg(avg_participant.c.ticket_count), 2)).scalar()

    return float(result) if result else 0.0




def get_full_stats(db : Session , id_organizer : int):

    general = get_general_value(db, id_organizer)
    monthly = get_monthly_stats(db, id_organizer)
    top_event = get_top_events(db,id_organizer)
    most_attended_event = get_most_attended_event(db,id_organizer)

    chart = get_daily_sales_chart(db,id_organizer)

    weekly_rev = sum(day["revenue"] for day in chart)
    avg_participant=get_avg_participant(db,id_organizer)

    def to_top_event(row):
        if not row:
            return None
        return TopEvent(
            id_event=row.id_event,
            name=row.name,
            value=float(row.val)
        )
    
    return DashboardStat(

        start_date= date.today() - timedelta(days=30),
        end_date= date.today(),

        active_events_count=general["active_events"],
        yearly_events_count= general["yearly_events"],
        potential_total_revenue=general["potential_revenue"],
        
        monthly_revenue=monthly["monthly_revenue"],
        monthly_events_count=monthly["monthly_events"],

        avg_participants=avg_participant,

        most_profitable_event= to_top_event(top_event["most_profitable"]),
        most_liked_event= to_top_event(top_event["most_liked"]),
        most_attended_event= to_top_event(most_attended_event["most_attended"]),

        daily_sales_chart=chart,
        weekly_total_revenue=weekly_rev


    )