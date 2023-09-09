from sqlalchemy import ForeignKey, Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Define the naming convention for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

# Create the metadata object with the naming convention
metadata = MetaData(naming_convention=convention)

# Create the base class for declarative models
Base = declarative_base(metadata=metadata)

# Define the many-to-many relationship table
company_dev = Table(
    'company_dev',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)

# Define the Company model
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    Freebie = relationship("Freebie", backref=backref("company"))
    devs = relationship("Dev", secondary=company_dev, back_populates="companies")

    def __repr__(self):
        return f'Company {self.name}, Founding year {self.founding_year}'

# Define the Dev model
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    Freebie = relationship("Freebie", backref=backref("dev"))
    companies = relationship("Company", secondary=company_dev, back_populates="devs")

    def __repr__(self):
        return f'<Dev {self.name}>'

# Define the Freebie model
class Freebie(Base):
    __tablename__ = "Freebie"

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    Value = Column(Integer())
    company_id = Column(Integer(), ForeignKey("companies.id"))
    dev_id = Column(Integer(), ForeignKey("devs.id"))

    def __repr__(self):
        return f'<Freebie {self.item_name}>'

# Create the engine and metadata objects
engine = create_engine('sqlite:///freebies.db')

# Create the tables in the database
Base.metadata.create_all(engine)