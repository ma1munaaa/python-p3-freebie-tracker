#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == "__main__":
    engine = create_engine("sqlite:///freebies.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Dev).delete()
    session.query(Company).delete()
    session.query(Freebie).delete()

    fake = Faker()
    
    # Populate Companies
    for _ in range(10):  # Create 10 fake companies
        company = Company(
            name=fake.company(),
            founding_year=fake.year(),
        )
        session.add(company)
    
    # Populate Devs
    for _ in range(15):  # Create 15 fake developers
        dev = Dev(
            name=fake.name(),
        )
        session.add(dev)

    # Populate Freebies
    for _ in range(30):  # Create 30 fake freebies
        freebie = Freebie(
            item_name=fake.word(),
            Value=fake.random_int(min=1, max=100),
            company_id=random.choice(session.query(Company).all()).id,  # Randomly assign a company
            dev_id=random.choice(session.query(Dev).all()).id,  # Randomly assign a developer
        )
        session.add(freebie)
    
    for company in session.query(Company).all():
        for dev in fake.random_elements(
            elements=session.query(Dev).all(),
            length=random.randint(1, 5),  # Random number of devs associated with each company
            unique=True,
        ):
            company.devs.append(dev)

    session.commit()
    session.close()