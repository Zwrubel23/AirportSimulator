import random
import json
import abc  # Python's built-in abstract class library
import sys


#region Date

class Index:
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4

    @staticmethod
    def getDay(day: str) -> int:
        if day == 'Monday':
            return 1
        elif day == 'Tuesday':
            return 2
        elif day == 'Wednesday':
            return 3
        elif day == 'Thursday':
            return 4
        elif day == 'Friday':
            return 5
        else:
            return -1

class Date:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    WEEK = [Monday, Tuesday, Wednesday, Thursday, Friday]
    def __init__(self):
        self.currDay: int = 1  # cumulative count of days in the simulation 
        self.currWeek: int = 1
        self.week_idx: int = 0  # index to get day of the week

    def new_day(self):
        self.currDay += 1
        if self.dayOfWeek is Date.Friday:
            self.currWeek += 1
            self.week_idx = 0
        else:
            self.week_idx += 1

    @property
    def week(self) -> int: return Date().currWeek
    @property
    def dayOfWeek(self) -> str: return Date.WEEK[self.week_idx]

    def __repr__(self): return f"{self.dayOfWeek}-{self.currWeek}"

#endregion


#region Airport
class Airport:
    def __init__(self, name: str, fly_chance_to: float, fly_chance_from: float, per_day_in: int, per_day_out: int):
        self.name: str = name
        self.fly_chance_to: float = fly_chance_to
        self.fly_chance_from: float = fly_chance_from
        self.per_day_in: int = per_day_in
        self.per_day_out: int = per_day_out
        
        if self.name == 'DIA':
            self.is_hub_airport: bool = True
        else:
            self.is_hub_airport: bool = False

        self.terminals: list[Terminal] = list()  # 
        self.current_travelers: list[Passenger] = list()

    def genTerminals(self):
        """Method to make the terminals at an airport."""
        pass

    def getName(self) -> str: return self.name

    def __repr__(self): return self.name

class AirportFactory:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    DIA = Airport(name='DIA', fly_chance_to=1, fly_chance_from=1, per_day_in=0, per_day_out=0)
    ORD = Airport(name='ORD', fly_chance_to=0.8, fly_chance_from=0.8, per_day_in=3, per_day_out=3)
    JFK = Airport(name='JFK', fly_chance_to=0.8, fly_chance_from=0.8, per_day_in=3, per_day_out=3)
    LAX = Airport(name='LAX', fly_chance_to=0.8, fly_chance_from=0.8, per_day_in=3, per_day_out=3)
    DFW = Airport(name='DFW', fly_chance_to=0.6, fly_chance_from=0.6, per_day_in=2, per_day_out=2)
    SFO = Airport(name='SFO', fly_chance_to=0.4, fly_chance_from=0.4, per_day_in=2, per_day_out=2)
    BOS = Airport(name='BOS', fly_chance_to=0.2, fly_chance_from=0.2, per_day_in=1, per_day_out=1)

    NUM_AIRPORTS: int = 7
    HUB_AIRPORT: Airport = DIA
    def __init__(self):
        self.airports: list[Airport] = [AirportFactory.DIA, AirportFactory.ORD, AirportFactory.JFK, AirportFactory.LAX, AirportFactory.DFW, AirportFactory.SFO, AirportFactory.BOS]
        self.airport_dict: dict = {
            'DIA': AirportFactory.DIA,
            'ORD': AirportFactory.ORD,
            'JFK': AirportFactory.JFK,
            'LAX': AirportFactory.LAX,
            'DFW': AirportFactory.DFW,
            'SFO': AirportFactory.SFO,
            'BOS': AirportFactory.BOS
        }

    def getAirports(self) -> list: return self.airports

    def getAirport(self, airport: str or Airport) -> Airport:
        # return self.airport_dict[airport]
        for ap in self.airports:
            if isinstance(airport, str):
                if ap.getName() == airport:
                    return ap
            if isinstance(airport, Airport):
                if ap == airport:
                    return ap
        return None

    def randomAirport(self, inc_hub: bool) -> Airport: 
        if not inc_hub:
            return random.choice(self.getAirports()[1:])
        else:
            return random.choice(self.getAirports())

#endregion


#region Airline
class Airline(object):
    __metaclass__ = abc.ABCMeta  # define abstract class
    @abc.abstractmethod
    def name() -> str: pass
    @abc.abstractmethod
    def abbr() -> str: pass
    @abc.abstractmethod
    def delay_chance() -> float: pass
    
class AmericanAirlines(Airline):
    def name() -> str: return "American Airlines"
    def abbr() -> str: return "AA"
    def delay_chance() -> float: return 0.04

class UnitedAirlines(Airline):
    def name() -> str: return "United Airlines"
    def abbr() -> str: return "UA"
    def delay_chance() -> float: return 0.03

class DeltaAirlines(Airline):
    def name() -> str: return "Delta Airlines"
    def abbr() -> str: return "DA"
    def delay_chance() -> float: return 0.01

class JetBlue(Airline):
    def name() -> str: return "Jet Blue Airlines"
    def abbr() -> str: return "JB"
    def delay_chance() -> float: return 0.02

#endregion


#region Passenger
class Namer:
    def __init__(self, n: list):
        self.names: list = n
        self.pass_: int = 1
        self.nextName: int = 0
    
    def getNext(self) -> str: 
        name: str = self.names[self.nextName]
        name = name + "_" + str(self.pass_)
        self.nextName += 1
        if self.nextName == len(self.names):
            self.nextName = 0
            self.pass_ = self.pass_ + 1
        return name

class Passenger:
    namelist: list = ["Deion", "Elanor", "Sam", "Anastasia", "Reid", "Britney", "Hockey Team", "Ralphie", "Football Team", "Baseball Team", "Basketball Team"]
    namer = Namer(namelist)
    def __init__(self, name: str=None, home_airprot: Airport=None): 
        if name is None:
            self.name = Passenger.namer.getNext()
        else:
            self.name = name

        self.currLocation: Airport = None
        self.flight: Flight = None
        self._home_airport: Airport = None
        self._preferred_airline: Airline = None  # None for now
        self.ticket: Ticket = None
        self.first_class_freq: float = .20
        self._pass_num: int = None  # cumulative count of passengers used for ticket

        if home_airprot is not None:
            self._home_airport = home_airprot

    # @property
    # def ticket(self) -> Ticket:
    #     return self._ticket
    # @ticket.setter
    # def ticket(self, newTicket: Ticket):
    #     self._ticket = newTicket

    @property
    def pass_number(self) -> int: return self._pass_num

    @property
    def home_airport(self) -> Airport: 
        return self._home_airport
    @home_airport.setter
    def home_airport(self, homeAirport: Airport): 
        self._home_airport = homeAirport

    @property
    def preferred_airline(self) -> Airline: 
        return self._preferred_airline
    @preferred_airline.setter
    def preferred_airline(self, prefferedAirline: Airline):
        self._preferred_airline = prefferedAirline

    def setLocation(self, newLocation: Airport):
        self.currLocation = newLocation

    def is_home(self) -> bool: self.currLocation == self.home_airport

    def __repr__(self): return self.name

class PassengerFactory:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    def __init__(self, amount: int):
        self.max_passengers: int = amount
        self.num_passengers: int = 0
        self.passengers: list[Passenger] = list()
        self.user: Passenger = None

    def createUser(self, name: str, home_airport: Airport):
        """Create the user."""
        self.user = Passenger(name, home_airport)
        self.user.setLocation(AirportFactory.DIA)
        self.user._pass_num = self.num_passengers
        self.num_passengers += 1
        self.passengers.append(self.user)

    def getPassenger(self, name: str) -> Passenger:
        """Query a passenger by name."""
        for passenger in self.passengers:
            if passenger.name == name:
                return passenger
        return None

    def createPassenger(self) -> Passenger:
        newPassenger: Passenger = Passenger()
        newPassenger.home_airport = AirportFactory().randomAirport(inc_hub=True)
        # newPassenger.setLocation(newPassenger.home_airport)  # what determines the starting location of passengers?
        newPassenger.setLocation(AirportFactory().HUB_AIRPORT)
        newPassenger._pass_num = self.num_passengers
        self.num_passengers += 1
        self.passengers.append(newPassenger)
        return newPassenger

#endregion


#region Airplane
class Airplane:
    def __init__(self):
        self.name = None
        self.manufacturer: Manufacturer = self.setManufacturer()
        self.airline: Airline = self.setAirline()
        self.currentAirport: Airport = None
        self.currentTerminal: Terminal = None
        self.max_capacity: int = 0
        self.first_class_seats: int = self.manufacturer.first_class_seats()
        self._break_down_prob: float = 0.0

    @property
    def break_down_prob(self) -> float:
        # self._break_down_prob += self.manufacturer.break_down_prob()
        # self._break_down_prob += self.airline.delay_chance()
        return self.manufacturer.break_down_prob() + self.airline.delay_chance()

    def setAirline(self):
        rand: int = random.random()
        if rand > .65:
            self.airline = AmericanAirlines()
        elif rand <= .65 and rand > .35:
            self.airline = UnitedAirlines()
        elif rand <= .5 and rand > .15:
            self.airline = DeltaAirlines()
        elif rand <= .15 and rand > .00:
            self.airline = JetBlue()

    def setManufacturer(self) -> 'Manufacturer':
        if random.random() > .55:
            self.manufacturer = Boeing()
        else:
            self.manufacturer = Airbus()

class AirplaneFactory:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    def __init__(self):
        self.num_american: int = 0
        self.num_united: int = 0
        self.num_delta: int = 0
        self.num_jetblue: int = 0

    # def numPlanes(self, airline)

    def createAirplane(self, airline: Airline) -> Airplane:
        airplane: Airplane = None
        if isinstance(airline, AmericanAirlines):
            self.num_american += 1
            airplane = Airplane()
        elif isinstance(airline, UnitedAirlines):
            self.num_united += 1
            airplane = Airplane()
        elif isinstance(airline, DeltaAirlines):
            self.num_delta += 1
            airplane = Airplane()
        elif isinstance(airline, JetBlue):
            self.num_jetblue += 1
            airplane = Airplane()
        return airplane

#endregion


#region Terminal
class Terminal:
    def __init__(self):
        self.airport: Airport = None
        self.airline: Airline = None
        self.name: str = None
        self.prev_flight: Flight = None
        self.curr_flight: Flight = None
        self.next_flight: Flight = None
        self.delay_chance: float = 0.0

class AmericanAirlinesTerminal(Terminal):
    def __init__(self, terminal: Terminal, newAirline: Airline):
        super().__init__()
        self.terminal = terminal
        self.prev_owner: Airline = terminal.getAirline()
        self.new_owner: Airline = newAirline
class UnitedAirlinesTerminal(Terminal):
    def __init__(self, terminal: Terminal, newAirline: Airline):
        super().__init__()
        self.terminal = terminal
        self.prev_owner: Airline = terminal.getAirline()
        self.new_owner: Airline = newAirline
class DeltaAirlinesTerminal(Terminal):
    def __init__(self, terminal: Terminal, newAirline: Airline):
        super().__init__()
        self.terminal = terminal
        self.prev_owner: Airline = terminal.getAirline()
        self.new_owner: Airline = newAirline
class JetBlueTerminal(Terminal):
    def __init__(self, terminal: Terminal, newAirline: Airline):
        super().__init__()
        self.terminal = terminal
        self.prev_owner: Airline = terminal.getAirline()
        self.new_owner: Airline = newAirline

# class NewTerminalOwner(Terminal):
#     """Employs the """
#     def __init__(self, terminal: Terminal, newAirline: Airline):
#         self.terminal = terminal
#         self.prev_owner: Airline = terminal.getAirline()
#         self.new_owner = newAirline


#endregion


#region Manufacturer
class Manufacturer:
    __metaclass__ = abc.ABCMeta  # define as abstract class
    @abc.abstractmethod
    def name() -> str: pass
    @abc.abstractmethod
    def break_down_prob() -> float: pass
    @abc.abstractmethod
    def first_class_seats() -> int: pass

class Boeing(Manufacturer):
    def name() -> str: return "Boeing"
    def break_down_prob() -> float: return 0.01
    def first_class_seats() -> int: return 10

class Airbus(Manufacturer):
    def name() -> str: return "Airbus"
    def break_down_prob() -> float: return 0.02
    def first_class_seats() -> int: return 14

#endregion


#region Flight
# TODO: 
# find good way to prevent more than X first class tickets from being created, 

class Flight:
    MAX_PASSENGERS: int = 20  # 300
    def __init__(self, origin: Airport, destination: Airport, week: int=None, day: str=None):
        self.plane: Airplane = None
        self.airline: Airline = None
        self.set_airline()
        self._flight_number: int = 0
        # how many first class tickets have been sold, check max # of first 
        # class on each flight by accessing flight.airplane.first_class_seats
        self.num_first_class: int = 0

        self.departure: Airport = origin
        self.departureTerminal: Terminal = None
        
        self.arrival: Airport = destination
        self.arrivalTerminal: Terminal = None

        self.currLocation: Airport = self.departure
        self.on_time: bool = None
        self.completed = False  # False if flight hasn't happened yet

        # Date of flight
        if week is None and day is None:
            self.date: Date = Date()
            self.week: int = Date().week  # week
            self.day: str = Date().dayOfWeek  # day
        else:
            self.date: Date = None
            self.week: int = week
            self.day: str = day

        self.passengers: list[Passenger] = list()
        

    def execute_flight(self) -> bool:
        """Execute the flight.  Move plane, passengers from origin airport to destination airport."""
        if self.completed:
            msg: str = f"Error: Flight {self.name} has already been completed."
            print(msg)
            return False
        # check for delays
        # check for mechanical issues
        # check for weather
        # allowed to execute the flight
        self.currLocation = self.arrival
        if self.num_passengers != 0:
            for traveler in self.passengers:
                if not traveler.ticket.is_valid():  # ticket is not valid
                    pass
                # each traveler has x% chance of missing their flight
                # miss_prob: float = 0.0
                # if random.random() <= miss_prob:
                #     pass
                # else:
                #     traveler.setLocation(self.arrival)
                traveler.setLocation(self.arrival)
        self.completed = True
        msg: str = f"Flight {self.name} tookoff from {self.departure.name} and landed in {self.arrival.name} with {self.num_passengers} passengers onboard."
        print(msg)
        return True


    def set_airline(self):
        prob: float = random.random()
        if prob >= .75:
            self.airline = AmericanAirlines()
        elif prob < .75 and prob >= .50:
            self.airline = UnitedAirlines()
        elif prob < .50 and prob >= .25:
            self.airline = DeltaAirlines()
        elif prob < .25:
            self.airline = JetBlue()

    @property
    def name(self) -> str:
        return f"{self.departure.getName()}_{self.arrival.getName()}_{self.flight_number}"

    @property
    def num_passengers(self) -> int: return len(self.passengers)

    def full_flight(self) -> bool: return len(self.passengers) == Flight.MAX_PASSENGERS

    def is_on_flight(self, traveler: Passenger) -> bool:
        for passenger in self.passengers:
            if passenger == traveler:
                return True
        return False

    def add_passenger(self, traveler: Passenger) -> bool:
        if self.is_on_flight(traveler):
            msg: str = f"{traveler.name} is already booked on the flight."
            print(msg)
        elif self.full_flight():
            msg: str = "Sorry this flight is fully booked"
            print(msg)
        else:
            self.passengers.append(traveler)
            if traveler.ticket.first_class:
                self.num_first_class += 1
            return True
        return False

    def first_class_available(self) -> bool:
        """Return if there are any first class seats left."""
        if self.plane is not None:
            return bool(self.num_first_class == self.plane.first_class_seats)
        else:
            return bool(self.num_first_class == 20)
    
    @property
    def flight_number(self) -> int: return self._flight_number
    @flight_number.setter
    def flight_number(self, newNumber: int): self._flight_number = newNumber

    @property
    def flight_log(self) -> dict:
        log: dict = {
            'Week': self.week,
            'Day': self.day,
            # 'Airline': self.airline.name(),
            'Name': self.name,
            'Departure': self.departure.name,
            # 'Departure Terminal': self.departureTerminal.name,
            'Arrival': self.arrival.name,
            # 'Arrival Terminal': self.arrivalTerminal.name,
            'Passengers': self.passengers.__len__(),
            'Passenger List': [traveler.name for traveler in self.passengers],
            'On Time': self.on_time,
            # 'Aircraft Manufacturer': self.plane.manufacturer.name(),
            # 'Date': self.date.__repr__(),
            # 'Week': self.date.week,
            # 'DayOfWeek': self.date.dayOfWeek,
            # 'SimulationDay': self.date.currDay,
            'Date': f"{self.day}-{self.week}",
            'Week': self.week,
            'DayOfWeek': self.day,
            'SimulationDay': ((self.week) * 5) + Index().getDay(self.day)
        }
        return log

    def show_flight_info(self):
        msg: str = f"Flight {self.name} on {self.week}-{self.day}."
        print(msg)

class FlightFactory:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    num_flights: int = 0
    def __init__(self):
        self.flight_log: list[Flight] = list()
    
    def createFlight(self, origin: Airport or str, destination: Airport or str, week: int=None, day: str=None) -> Flight:
    # def createFlight(self, origin: Airport or str, destination: Airport or str) -> Flight:
        if isinstance(origin, str):
            origin = AirportFactory.getAirport(origin)
        if isinstance(destination, str):
            destination = AirportFactory.getAirport(destination)

        if week is None and day is None:
            week, day = Date().week, Date().dayOfWeek
        #     flight: Flight = Flight(origin, destination, week, day)
        # else:
        #     flight: Flight = Flight(origin, destination)
        flight: Flight = Flight(origin, destination, week, day)

        flight.flight_number = FlightFactory.num_flights
        self.flight_log.append(flight)
        FlightFactory.num_flights += 1
        msg: str = f"Scheduled flight {flight.name} on {flight.week}-{flight.day}."
        print(msg)
        return flight

    def log_flight_to_file(self) -> bool: 
        """Add the flight to the external file."""
        return False

    # --- Utility methods ---
    def getFlightsBetween(self, origin: Airport, dest: Airport, week: int=None, day: str=None) -> 'list[Flight]':
        if week is None and day is None:
            week, day = Date().week, Date().dayOfWeek
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.departure == origin and flight.arrival == dest and flight.week == week and flight.day == day:
                flights.append(flight)
        return flights

    def getFlightsByDate(self, week: int=None, day: str=None) -> 'list[Flight]':
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.week == week and flight.day == day:
                flights.append(flight)
            elif flight.week == week and day is None:
                if flight.week == week:
                    flights.append(flight)
        return flights


    def getFlight(self, origin: Airport, week: int, day: str) -> 'list[Flight]': 
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.departure == origin and flight.week == week and flight.day == day:
                flights.append(flight)
        return flights

    def getFlightByOrigin(self, airport: Airport) -> 'list[Flight]': 
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.departure == airport:
                flights.append(flight)
        return flights

    def getFlightByOrigin(self, airport: Airport, week: int=None, day: str=None) -> 'list[Flight]': 
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if week == None and day != None:
                if flight.departure == airport and flight.day == day:
                    flights.append(flight)
            elif week != None and day == None:
                if flight.departure == airport and flight.week == week:
                    flights.append(flight)
            elif week == None and day == None:
                if flight.departure == airport:
                    flights.append(flight)
            else:
                if flight.departure == airport and flight.week == week and flight.day == day:
                    flights.append(flight)
        return flights

    def getFlightByDestination(self, airport: Airport) -> 'list[Flight]': 
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.arrival == airport:
                flights.append(flight)
        return flights
    
    def getFlightByDestination(self, airport: Airport, week: int=None, day: str=None) -> 'list[Flight]':
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if week == None and day != None:
                if flight.arrival == airport and flight.day == day:
                    flights.append(flight)
            elif week != None and day == None:
                if flight.arrival == airport and flight.week == week:
                    flights.append(flight)
            elif week == None and day == None:
                if flight.arrival == airport:
                    flights.append(flight)
            else:
                if flight.arrival == airport and flight.week == week and flight.day == day:
                    flights.append(flight)
        return flights
    
    def getFlightByAirline(self, airline: Airport) -> 'list[Flight]': 
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.airline == airline:
                flights.append(flight)
        return flights

#endregion


#region Ticket
class Ticket:
    def __init__(self, flight: Flight, traveler: Passenger):
        self.traveler: Passenger = traveler
        self.flight: Flight = flight
        self.airline: Airline = flight.airline
        self.origin: Airport = flight.departure
        self.terminal: Terminal = flight.departureTerminal
        self.destination: Airport = flight.arrival
        self.first_class: bool = False
        # Date of flight
        self.date: Date = flight.date  # Date()
        self.week: int = flight.week  # Date().week
        self.day: str = flight.day  # Date().dayOfWeek

    @property
    def ticket_id(self) -> str: 
        return f"{self.origin.getName()[0]}{self.destination.getName()[0]}-{self.flight.flight_number}-{self.traveler.pass_number}-{self.week}{self.day[0]}"

    @property
    def ticket_log(self) -> dict:
        """Make the ticket that will be stored in TicketLog.json"""
        log: dict = {
            'Passenger': self.traveler.name,
            'Flight': self.flight.name,
            'Departure': self.origin.getName(),
            'Arrival': self.destination.getName(),
            'Flight Number': self.flight.flight_number,
            # 'Airline': self.airline.name(),
            'First Class': self.first_class,
            'Date': self.date,
            'Week': self.week,
            'DayOfWeek': self.day,
            'TicketID': self.ticket_id
        }
        return log

    def is_first_class(self) -> bool: return self.first_class

    def is_valid(self) -> bool:
        return all([
            self.traveler.currLocation == self.origin,
            self.traveler.currLocation == self.flight.departure,
            self.origin == self.flight.departure,
            self.destination == self.flight.departure,
            self.terminal == self.flight.departureTerminal,
            self.flight.date == self.date,
            self.first_class == False
        ])

class TicketDecorator(Ticket):
    """Decorator method"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, ticket):
        self.ticket = ticket
    
    @abc.abstractmethod
    def is_valid(self) -> bool: pass

class FirstClassTicket(TicketDecorator):
    """Decorator method"""
    def __init__(self, ticket: Ticket):
        super(ticket)
        # super(ticket)  # which one?
        self.first_class: bool = True

    def is_valid(self) -> bool:
        return all([
            self.traveler.currLocation == self.origin,
            self.traveler.currLocation == self.flight.departure,
            self.origin == self.flight.departure,
            self.destination == self.flight.departure,
            self.terminal == self.flight.departureTerminal,
            self.flight.date == self.date,
            self.first_class == True
        ])
    
class TicketFactory:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    def __init___(self):
        self.tickets: list[Ticket] = []

    def createTicket(self, flight: Flight, traveler: Passenger, first_class: bool=False) -> Ticket:
        newTicket: Ticket = Ticket(flight, traveler)
        if first_class:
            # to get here flight.first_class_available() must  be true
            newTicket = FirstClassTicket(newTicket)  # Decorator method
        return newTicket
    

#endregion


#region Logger
class Logger:
    """Subject aka Observable or Publisher"""
    def __init__(self, filename: str):
        self.filename: str = filename

    def write_to_file(self, newLog: dict):
        """Opens and reads a JSON file and adds the dictionary to the file."""
        # OLD
        # with open(self.filename, 'a') as file:
        #     # json.dump(newLog, file)
        #     file.write(json.dumps(newLog))

        # 1. Read file contents
        with open(self.filename, 'r') as file:
            data: list = json.load(file)
        # 2. Update json object
        data.append(newLog)
        # 3. Write json file
        with open(self.filename, 'w') as file:
            json.dump(data, file)

    def register_observer(self, observer): raise NotImplementedError
    def remove_observer(self, observer): raise NotImplementedError
    def notify_observers(self): raise NotImplementedError
    def condition_changed(self): raise NotImplementedError

class Observer:
    """Observer aka Subscriber"""
    def update(self, flight_log): raise NotImplementedError

class FlightLogger(Logger):
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        # it.__init__(*args, **kwds)
        return it
    
    def __init__(self):
        super().__init__(filename='FlightLog.json')
        self.observers: list[Observer] = []  # list of instances using the FlightLogger
        self.flight_log: list[Flight] = []
    
    def register_observer(self, observer: Observer): self.observers.append(observer)
    def   remove_observer(self, observer: Observer): self.observers.remove(observer)

    def notify_observers(self): 
        """new_ticket()
        Previously notify_observers"""
        for observer in self.observers:
            observer.update(self.flight_log)
    
    def condition_changed(self):
        currFlight: Flight = self.flight_log[-1]
        self.write_to_file(currFlight.flight_log)
        self.notify_observers()

    def update(self, newFlight: Flight, write: bool=True):
        self.flight_log.append(newFlight)
        # if write:
            # self.condition_changed()
        self.condition_changed()
    
    def add(self, newFlight: Flight):
        self.flight_log.append(newFlight)

class TicketLogger(Logger):
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        # it.__init__(*args, **kwds)
        return it

    def __init__(self):
        super().__init__(filename='TicketLog.json')
        self.observers: list[Observer] = []  # list of instances using the TicketLogger
        self.ticket_log: list[Ticket] = []
    
    def register_observer(self, observer: Observer): self.observers.append(observer)
    def   remove_observer(self, observer: Observer): self.observers.remove(observer)
    
    def notify_observers(self): 
        """new_ticket()
        Previously notify_observers"""
        for observer in self.observers:
            observer.update(self.ticket_log)

    def condition_changed(self): 
        currTicket: Ticket = self.ticket_log[-1]
        self.write_to_file(currTicket.ticket_log)
        self.notify_observers()
    
    def update(self, newTicket: Ticket, write: bool=True):
        self.ticket_log.append(newTicket)
        # if write:
            # self.condition_changed()
        self.condition_changed()
    
    def add(self, newTicket: Ticket):
        self.ticket_log.append(newTicket)

#endregion


#region AirTrafficControl
class AirTrafficControl:
    """Class for orchestrating flights with passengers, between airports & terminals."""
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
        
    def __init__(self, flightLog: FlightLogger, ticketLog: TicketLogger):
        self.currDay: int = 1
        self.currWeek: int = 1
        self.day: str = "Monday"

        self.flightLog: FlightLogger = flightLog
        self.ticketLog: TicketLogger = ticketLog

        self.passengerFactory = PassengerFactory(amount=100)
        self.airplaneFactory = AirplaneFactory()
        self.airportFactory = AirportFactory()
        self.flightFactory = FlightFactory()
        self.ticketFactory = TicketFactory()
        
        self.airports: list[Airport] = self.airportFactory.getAirports()
        self.passengers: list[Passenger] = list()
        self.all_flights: list[Flight] = list()
        self.HUB_AIRPORT: Airport = self.airportFactory.HUB_AIRPORT

        self.master_schedule: list[Flight] = list()

        self.createPassengers()
    
    def createPassengers(self):
        msg: str = "> Creating passengers...."
        print(msg)
        for i in range(self.passengerFactory.max_passengers):
            new_passenger: Passenger = self.passengerFactory.createPassenger()
            self.passengers.append(new_passenger)
        
    @property
    def allow_remote_booking(self) -> bool:
        """Whether to allow passengers to book a flight when they aren't at the departure airport."""
        return True

    def schedule_day(self, week: int=None, day: str=None):
        """Method to schedule a day's worth of flights at all airports."""
        if week is None and day is None:
            week, day = Date().week, Date().dayOfWeek
        low_chance: int = 5  # the higher this number the better(?) the chance of an extra flight
        high_chance: int = 90  # the higher this number the better the chance an extra flight will be scheduled
        d_t_a: float = random.randint(low_chance, high_chance) / 100
        a_t_d: float = random.randint(low_chance, high_chance) / 100

        # loop through airports
        # for airport in self.airports:
        for i in range(len(self.airports)):
            airport: Airport = self.airports[i]
            if airport.is_hub_airport:  # not hub airport
                continue
            flight: Flight = None

            # ----- add daily flights in  -----
            for i in range(airport.per_day_in):
                flight = self.flightFactory.createFlight(origin=self.airportFactory.HUB_AIRPORT, destination=airport, week=week, day=day)
                self.master_schedule.append(flight)
            # add random chances of each airport getting extra flights 
            if airport.fly_chance_to >= d_t_a:
                flight = self.flightFactory.createFlight(origin=self.airportFactory.HUB_AIRPORT, destination=airport, week=week, day=day)
                self.master_schedule.append(flight)

            # ----- add daily flights out -----
            for i in range(airport.per_day_out):
                flight = self.flightFactory.createFlight(origin=airport, destination=self.airportFactory.HUB_AIRPORT, week=week, day=day)
                self.master_schedule.append(flight)
            # add random chances of each airport getting extra flights 
            if airport.fly_chance_from >= a_t_d:
                flight = self.flightFactory.createFlight(origin=airport, destination=self.airportFactory.HUB_AIRPORT, week=week, day=day)
                self.master_schedule.append(flight)
        msg: str = f"All flights scheduled for {day}, week {week}"
        print(msg)

    def book_flight(self, passenger_name: str, origin: str or Airport, dest: str or Airport, day: str, week: int, confirm_msg: bool=False) -> bool:
        """Method to book a flight for a passenger."""
        if not isinstance(origin, Airport):
            origin: Airport = self.airportFactory.getAirport(origin)
        if not isinstance(dest, Airport):
            dest: Airport = self.airportFactory.getAirport(dest)

        if origin == dest:  # can't book flight to and from same airport
            msg: str = f"Error: Can't book flight to and from same airport {origin} -> {dest}."
            print(msg)
            return False

        traveler: Passenger = self.passengerFactory.getPassenger(passenger_name)
        if not self.allow_remote_booking:
            if traveler.currLocation == origin:
                msg: str = "Error: You cannot book a flight"
                print(msg)

        # get the flight object
        # NOTE: Just to speed up the loop below
        # flight_lst: list[Flight] = self.flightFactory.getFlightsBetween(origin, dest, week, day)
        if origin.name == "DIA" or origin.is_hub_airport:
            # flights out of DIA on the specific day and week
            flight_lst: list[Flight] = self.flightFactory.getFlightByOrigin(origin, week, day)
        else:
            # flights into DIA on the specific day and week
            flight_lst: list[Flight] = self.flightFactory.getFlightByDestination(dest, week, day)

        # 1. find an available flight within the flight list
        for flight in flight_lst:
            if flight.full_flight():
                continue  # Flight is full
            if flight.departure == origin and flight.arrival == dest:            
                # 2. check passenger isn't already on flight
                if flight.is_on_flight(traveler):
                    msg: str = f"Error: Passenger {traveler.name} is already booked on flight {flight.name}."
                    print(msg)
                    return True
                # 3. Create ticket
                ticket: Ticket = None
                # Verify there are/are not first class seats available
                if flight.first_class_available() and traveler.first_class_freq > random.random():  # First Class Ticket
                    ticket = self.ticketFactory.createTicket(flight, traveler, first_class=True)
                else:  # Economy Ticket
                    ticket = self.ticketFactory.createTicket(flight, traveler, first_class=False)
                traveler.ticket = ticket  # give the traveler their ticket
                self.ticketLog.update(ticket, write=True)

                # 4. add traveler to flight
                flight.add_passenger(traveler)
                traveler.flight = flight  # set the travelers flight to the current on one
                if confirm_msg:
                    msg: str = f"Successfully booked ticket from {origin} to {dest} for {traveler} on flight {flight.name}"
                    print(msg)
                    # print(f" on flight {flight.name}")
                return True
        if confirm_msg:
            # print(flight.departure, origin, flight.arrival, dest)
            # print(origin, dest)
            msg: str = f"Error({len(flight_lst)}): A flight from {origin} to {dest} on {week}-{day} is not available for {passenger_name}."
            print(msg)
        return False

    def allow_flights_takeoff(self):
        # day_flights: list[Flight] = self.atc.flightFactory.getFlightsByDate(self.currWeek, day)
        pass

    def display_flights(self, week: int=None): 
        """Print the flights with passengers booked on them."""
        msg: str = f"~~~~~ Flight Display Week {week} ~~~~~"
        print(msg)
        if week is None:
            week = Date().currWeek
        for flight in self.master_schedule:
            if flight.week == week and len(flight.passengers) > 0:
                print(flight.flight_log)
        msg: str = f"~~~~~ End Flight Display Week {week} ~~~~~"
        print(msg)
    
    def take_off(self):
        """Perform all the operations necessary to get all the planes from 
        origin to the destination."""
        pass

#endregion


#region Simulator
class Simulator:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    # FINAL_WEEK = 4
    def __init__(self, weeks: int=4):
        self.__num_weeks: int = weeks  # number of weeks to run the simulation
        self.dayCount: int = 1
        self.currWeek: int = 1
        self.date = Date()
        self.flightLog: FlightLogger = FlightLogger()
        self.ticketLog: TicketLogger = TicketLogger()
        self.atc: AirTrafficControl = AirTrafficControl(self.flightLog, self.ticketLog)

    def show_travelers(self):
        print('i \tName \tLocation \tHome Airport')
        for i, traveler in enumerate(self.atc.passengers):
            print(i, traveler.name, traveler.currLocation, traveler.home_airport)

    @property
    def FINAL_WEEK(self) -> int: return self.__num_weeks

    def get_option(self, day: Date.dayOfWeek):
        # get name
        name: str = input("Enter your name: ")
        # get home airport
        print("Choose a home airport: ")
        for ap in self.atc.airports:
            print(ap)
        home: str = input("Enter your home airport: ")
        home_airport: Airport = self.atc.airportFactory.getAirport(home)
        self.atc.passengerFactory.createUser(name, home_airport)
        user: Passenger = self.atc.passengerFactory.user

        print(f"Current location: {user.currLocation.getName()}")
        print(f"Current Day: {day}, Week {self.currWeek}, Day {self.dayCount}")
        # show available flights
        print("Available Flights: ")
        available_flights: list[Flight] = self.atc.flightFactory.getFlightByOrigin(home_airport, self.currWeek, day)
        for i, flight in enumerate(available_flights, start=1):
            print(f"{i}. {flight.show_flight_info()}")
        choice: int = int(input("Which number flight would you like to choose? "))
        usr_flight: Flight = available_flights[choice]

        origin: Airport = usr_flight.departure
        dest: Airport = usr_flight.arrival
        flight: Flight = self.atc.book_flight(passenger_name=user.name, origin=origin, dest=dest, day=day, week=self.currWeek, confirm_msg=True)
        

    def run_simulation(self):
        print("<<<<< New Simulation >>>>>")
        # iterate through weeks until final week is reached
        while self.currWeek <= self.FINAL_WEEK:
            self.schedule_new_week()

            # iterate through the days of the week
            for day in Date.WEEK:
                self.book_new_day(day)  # book passengers on flights
                self.execute_day(day)  # flights fly passengers to destination

            self.end_week()
            print("\n\n")
        self.end_simulation()

    def end_simulation(self):
        print("<<<<< End Simulation >>>>>")

    def end_week(self):
        print(f"********** End Week {self.currWeek} **********")
        Date().new_day()
        self.currWeek += 1

    def schedule_new_week(self):
        print(f"********** Week {self.currWeek} **********")
        for day in Date.WEEK:
            self.schedule_new_day(day)

    def schedule_new_day(self, day: str):
        print(f"***** {day} *****")
        print("Scheduling flights....")
        self.atc.schedule_day(self.currWeek, day)
        self.dayCount += 1

    def go_home(self, day: str):
        """Commands for all travelers to book flights to their home airports."""
        for traveler in self.atc.passengers:
            ap: Airport = traveler.home_airport
            if ap == traveler.currLocation:
                continue
            flight: Flight = self.atc.book_flight(
                passenger_name=traveler.name, 
                # origin=traveler.currLocation.getName(), 
                # dest=ap.getName(), 
                origin=traveler.currLocation.getName(), 
                dest=ap.getName(), 
                day=day, 
                week=self.currWeek, 
                confirm_msg=True
            )

    def book_new_day(self, day: str):
        """Perform operations necessary for booking the passengers flights."""
        print(f"---------- Booking [{day}] ----------")
        for traveler in self.atc.passengers:
            # ap: Airport = self.atc.airportFactory.randomAirport(inc_hub=False)

            if traveler.currLocation.getName() == 'DIA':  # DIA -> ___
                origin: Airport = self.atc.airportFactory.HUB_AIRPORT
                dest: Airport = self.atc.airportFactory.randomAirport(inc_hub=False)
            else:  # ___ -> DIA
                origin: Airport = traveler.currLocation
                dest: Airport = self.atc.airportFactory.HUB_AIRPORT

            success: bool = self.atc.book_flight(
                passenger_name=traveler.name, 
                origin=origin, 
                dest=dest, 
                day=day, 
                week=self.currWeek, 
                confirm_msg=True
            )
        print(f"---------- Finished Booking [{day}] ----------")

    def execute_day(self, day: str):
        """Perform the operations for executing a day's worth of flights."""
        print(f"===== Executing {day} =====")
        day_flights: list[Flight] = self.atc.flightFactory.getFlightsByDate(self.currWeek, day)
        for flight in day_flights:
            # print(flight.name, flight.day, flight.week)
            if flight.num_passengers == 0:
                continue
            flight.execute_flight()
            # at this point the current flight is already done
            self.flightLog.update(flight, write=True)
        print(f"===== Finished Executing {day} =====")

    def execute_week(self):
        """Perform the operations for executing the week's worth of flights."""
        print(f"===== Executing Week {self.currWeek} =====")
        week_of_flights = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': []
        }
        for flight in self.atc.master_schedule:
            week_of_flights[flight.day].append(flight)
        
        for day, flight_lst in week_of_flights.items():
            print(f"=== {day} ===")
            for flight in flight_lst:
                flight.execute_flight()

        # for flight in self.atc.master_schedule:
            # flight.execute_flight()
        print(f"=====  Finished Week {self.currWeek} =====")

#endregion



if __name__ == "__main__":
    # File is run from command line.
    # Save the simulation output to the SimResults file.
    sim: Simulator = Simulator(weeks=1)

    original_stdout = sys.stdout  # Save a reference to the original standard output
    with open('SimResults.txt', 'w') as file:
        sys.stdout = file  # Change the standard output to SimResults.txt
        sim.run_simulation()
        sys.stdout = original_stdout  # Reset the standard output to its original value

else:  # Imported as a Module
    pass

