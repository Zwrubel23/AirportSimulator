"""Airport Simulator
By Zach Wrubel & Thor Breece
CSCI 4448
Spring 2023

Check README for relevant information.
"""
import random
import json
import abc  # Python's built-in abstract class library
import sys


#region Constants

class Const:
    """Store for constant values"""
    numWeeks: int = 1
    # Maximum number of passengers that can fit on a flight
    max_passengers: int = 25  # 300
    # Number of travelers in the simulation
    max_travelers: int = 100
    # Maximum number of terminals at an airport
    max_terminals: int = 50
#endregion


#region Date

class Date:
    """Class to keep track of date in one spot."""
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
    """Airport representation.  Only 7 Airport objects will be created."""
    def __init__(self, name: str, fly_chance_to: float, fly_chance_from: float, per_day_in: int, per_day_out: int, poor_weather: float):
        self.name: str = name
        self.fly_chance_to: float = fly_chance_to  # probability extra flight into airport is added 
        self.fly_chance_from: float = fly_chance_from  # probability extra flight out of airport is added 
        self.per_day_in: int = per_day_in  # flights into the airport each day
        self.per_day_out: int = per_day_out  # flights out of the airport each day 
        self.poor_weather_prob: float = poor_weather  # probability airport weather is too poor for planes to take off
        
        if self.name == 'DIA':
            self.is_hub_airport: bool = True
        else:
            self.is_hub_airport: bool = False

        # self.terminalFactory = TerminalFactory()
        self.terminals: list[Terminal] = list()
        self.current_travelers: list[Passenger] = list()
        self.planes: list[Airplane] = list()  # list of planes currently at the airport

    def removePlane(self, airplane: 'Airplane'):
        """Remove given airplane from airport's list of planes"""
        try:
            self.planes.remove(airplane)
        except ValueError:
            for i, plane in enumerate(self.planes):
                if plane.name == airplane.name:
                    self.planes.remove(airplane)
    def addPlane(self, airplane: 'Airplane'): self.planes.append(airplane)

    def get_planes_by_airline(self, airline: 'Airline') -> 'list[Airplane]':
        """Get a list of the airplanes currently at the airport by airline"""
        currPlanes: list[Airplane] = list()
        for plane in self.planes:
            if plane.airline.name() == airline.name():
                currPlanes.append(plane)
        return currPlanes

    def getName(self) -> str: return self.name
    def __repr__(self): return self.name

class AirportFactory:
    """Factory to handle and control creation and accessing airport objects."""
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    DIA = Airport(name='DIA', fly_chance_to=1.0, fly_chance_from=1.0, per_day_in=0, per_day_out=0, poor_weather=0.10)
    ORD = Airport(name='ORD', fly_chance_to=0.8, fly_chance_from=0.8, per_day_in=3, per_day_out=3, poor_weather=0.08)
    JFK = Airport(name='JFK', fly_chance_to=0.8, fly_chance_from=0.8, per_day_in=3, per_day_out=3, poor_weather=0.05)
    LAX = Airport(name='LAX', fly_chance_to=0.8, fly_chance_from=0.8, per_day_in=3, per_day_out=3, poor_weather=0.02)
    DFW = Airport(name='DFW', fly_chance_to=0.6, fly_chance_from=0.6, per_day_in=2, per_day_out=2, poor_weather=0.01)
    SFO = Airport(name='SFO', fly_chance_to=0.4, fly_chance_from=0.4, per_day_in=2, per_day_out=2, poor_weather=0.04)
    BOS = Airport(name='BOS', fly_chance_to=0.2, fly_chance_from=0.2, per_day_in=1, per_day_out=1, poor_weather=0.05)

    NUM_AIRPORTS: int = 7
    HUB_AIRPORT: Airport = DIA
    def __init__(self):
        self.airports: list[Airport] = [AirportFactory.DIA, AirportFactory.ORD, AirportFactory.JFK, AirportFactory.LAX, AirportFactory.DFW, AirportFactory.SFO, AirportFactory.BOS]

    def getAirports(self) -> 'list[Airport]': return self.airports

    def getAirport(self, airport: str or Airport) -> Airport:
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
    """Base Airline class."""
    __metaclass__ = abc.ABCMeta  # define abstract class
    @abc.abstractmethod
    def name(self) -> str: pass
    @abc.abstractmethod
    def abbr(self) -> str: pass
    @abc.abstractmethod
    def delay_chance(self) -> float: pass
    @abc.abstractmethod
    def flies_to(self, airport: Airport or str) -> bool: pass
    
class AmericanAirlines(Airline):
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    def name(self) -> str: return "American Airlines"
    def abbr(self) -> str: return "AA"
    def delay_chance(self) -> float: return 0.04
    def flies_to(self, airport: Airport or str) -> bool:
        return airport.getName() in ['DIA','ORD','JFK','LAX','DFW','SFO']

class UnitedAirlines(Airline):
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    def name(self) -> str: return "United Airlines"
    def abbr(self) -> str: return "UA"
    def delay_chance(self) -> float: return 0.03
    def flies_to(self, airport: Airport or str) -> bool:
        return airport.getName() in ['DIA','ORD','LAX','DFW','SFO']

class DeltaAirlines(Airline):
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    def name(self) -> str: return "Delta Airlines"
    def abbr(self) -> str: return "DA"
    def delay_chance(self) -> float: return 0.01
    def flies_to(self, airport: Airport or str) -> bool:
        return airport.getName() in ['DIA','JFK','SFO','BOS']

class JetBlue(Airline):
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    def name(self) -> str: return "Jet Blue Airlines"
    def abbr(self) -> str: return "JB"
    def delay_chance(self) -> float: return 0.02
    def flies_to(self, airport: Airport or str) -> bool:
        return airport.getName() in ['DIA','LAX','BOS']

#endregion


#region Passenger

class Namer:
    """Namer class to handle giving passengers similar but unique names."""
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
    """Passenger class to represent an individual in the simulation.  
    Tracks traveler/passenger location, current flight & ticket, and 
    determines first class probability."""
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
        self.ticket: Ticket = None
        self.first_class_freq: float = .20
        self._pass_num: int = None  # cumulative count of passengers used for ticket
        self.is_user: bool = False  # only true if passenger is the user

        if home_airprot is not None:
            self._home_airport = home_airprot

    @property
    def pass_number(self) -> int: return self._pass_num

    @property
    def home_airport(self) -> Airport: 
        return self._home_airport
    @home_airport.setter
    def home_airport(self, homeAirport: Airport): 
        self._home_airport = homeAirport

    def is_team(self) -> bool:
        """Check if the passenger is a team. They're not allowed to book first class seats."""
        return 'Team' in self.name

    def setLocation(self, newLocation: Airport): self.currLocation = newLocation

    def is_home(self) -> bool: self.currLocation == self.home_airport

    def __repr__(self): return self.name

class PassengerFactory:
    """Factory to handle traveler/passenger creation and accessing."""
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
        newPassenger.setLocation(newPassenger.home_airport)  # what determines the starting location of passengers?
        # newPassenger.setLocation(AirportFactory().HUB_AIRPORT)
        newPassenger._pass_num = self.num_passengers
        self.num_passengers += 1
        self.passengers.append(newPassenger)
        return newPassenger

#endregion


#region Manufacturer

class Manufacturer:
    """Airplane Manufacturer base class."""
    __metaclass__ = abc.ABCMeta  # define as abstract class
    @abc.abstractmethod
    def name(self) -> str: pass
    @abc.abstractmethod
    def break_down_prob(self) -> float: pass
    @abc.abstractmethod
    def num_seats(self) -> int: pass
    @abc.abstractmethod
    def first_class_seats(self) -> int: pass

class Boeing(Manufacturer):
    def name(self) -> str: return "Boeing"
    def break_down_prob(self) -> float: return 0.01
    def num_seats(self) -> int: return Const.max_passengers
    def first_class_seats(self) -> int: return 10

class Airbus(Manufacturer):
    def name(self) -> str: return "Airbus"
    def break_down_prob(self) -> float: return 0.02
    def num_seats(self) -> int: return Const.max_passengers + 5
    def first_class_seats(self) -> int: return 14

#endregion


#region Airplane

class Airplane:
    """Represents an airplane object. Tracks current location, manufacturer 
    and airline operating aircraft.  Also determines probability of breaking 
    down with Strategy Pattern"""
    def __init__(self, number: int):
        self.plane_num: int = number  # number unique to each plane 
        self.airline: Airline = None
        self.manufacturer: Manufacturer = None
        self.setManufacturer()  # Strategy pattern

        self.currentAirport: Airport = None
        self.currentTerminal: Terminal = None
        self.max_capacity: int = self.manufacturer.num_seats()
        self.first_class_seats: int = self.manufacturer.first_class_seats()

    @property
    def name(self) -> str: return f"{self.airline.abbr()}-{self.plane_num}"

    @property
    def break_down_prob(self) -> float:
        return self.manufacturer.break_down_prob() + self.airline.delay_chance()

    def setManufacturer(self):
        """Part of Strategy Pattern, sets airline at object creation when 
        method is called from init."""
        if isinstance(self.airline, UnitedAirlines):
            if random.random() > .50:
                self.manufacturer = Boeing()
            else:
                self.manufacturer = Airbus()
        elif isinstance(self.airline, (AmericanAirlines, JetBlue)):
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
        self.planes: list[Airplane] = list()

    @property
    def num_planes(self) -> int: return self.num_american + self.num_united + self.num_delta + self.num_jetblue

    def createAirplane(self, airline: Airline) -> Airplane:
        airplane: Airplane = None
        if isinstance(airline, AmericanAirlines):
            self.num_american += 1
            airplane = Airplane(number=self.num_planes)
        elif isinstance(airline, UnitedAirlines):
            self.num_united += 1
            airplane = Airplane(number=self.num_planes)
        elif isinstance(airline, DeltaAirlines):
            self.num_delta += 1
            airplane = Airplane(number=self.num_planes)
        elif isinstance(airline, JetBlue):
            self.num_jetblue += 1
            airplane = Airplane(number=self.num_planes)
        airplane.airline = airline
        self.planes.append(airplane)
        return airplane

#endregion


#region Terminal

class Terminal:
    def __init__(self, terminal_number: int):
        self.airport: Airport = None
        # self.airline: Airline = None
        self.airlines: list[Airline] = list()  # list of airlines that have operated at this terminal
        # self.name: str = None

        # self.prev_flight: Flight = None
        self.curr_flight: Flight = None
        # self.next_flight: Flight = None

        # departing_flight is the flight physically at the terminal, 
        # while arriving_flight is the flight that will be at the terminal next.
        self.arriving_flight: Flight = None  # goes to destinationTerminal / arrivalTerminal
        self.departing_flight: Flight = None  # goes to originTerminal / departureTerminal
        self.flight_docked: Flight = None  # flight currently at the terminal

        # self.delay_chance: float = 0.0
        self.terminal_number: int = terminal_number

    def setTerminalNumber(self, number: int): self.terminal_number = number

    def getTerminalNumber(self) -> int:
        for i, terminal in enumerate(self.airport.terminals):
            if terminal == self:
                return i
        return -1

    @property
    def name(self) -> str: return f"{self.airport.getName()}_T-{self.terminal_number}"

    def arrival_available(self) -> bool: return self.arriving_flight is None
    def departure_available(self) -> bool: return self.departing_flight is None
    def is_available(self) -> bool: 
        # return self.curr_flight == None
        return self.arriving_flight is None

    def flight_departed(self): self.curr_flight = None
    def flight_arrived(self, newFlight: 'Flight'): self.curr_flight = newFlight

    def curr_airline(self) -> Airline: return self.curr_flight.airline

    def acceptable_airline(self, airline: Airline) -> bool: return airline in self.airlines
    
    def __repr__(self) -> str: return self.name
    
    @property
    def delay_chance(self) -> float: 
        # return self.airline.delay_chance()
        return self.curr_flight.airline.delay_chance()

class NewTerminalOperator(Terminal):
    """Use the decorator pattern to add airlines to terminals."""
    def __init__(self, terminal: Terminal):
        super().__init__(terminal.terminal_number)
        self.terminal = terminal
        self.airport = terminal.airport
        # self.curr_flight = self.terminal.curr_flight

    def curr_airline(self) -> Airline: raise NotImplementedError
    # def acceptable_airline(self, airline: Airline) -> bool: raise NotImplementedError

class AmericanAirlinesTerminal(NewTerminalOperator):
    def __init__(self, terminal: Terminal):
        super().__init__(terminal)
        self.terminal = terminal
        self.airlines.append(self.curr_airline())
    def curr_airline(self) -> Airline: 
        return AmericanAirlines()
    # def acceptable_airline(self, airline: Airline) -> bool: return airline.abbr() == "AA"
        
class UnitedAirlinesTerminal(NewTerminalOperator):
    def __init__(self, terminal: Terminal):
        super().__init__(terminal)
        self.terminal = terminal
        self.airlines.append(self.curr_airline())
    def curr_airline(self) -> Airline: 
        return UnitedAirlines()
    # def acceptable_airline(self, airline: Airline) -> bool: return airline.abbr() == "UA"

class DeltaAirlinesTerminal(NewTerminalOperator):
    def __init__(self, terminal: Terminal):
        super().__init__(terminal)
        self.terminal = terminal
        self.airlines.append(self.curr_airline())
    def curr_airline(self) -> Airline: 
        return DeltaAirlines()
    # def acceptable_airline(self, airline: Airline) -> bool: return airline.abbr() == "DA"

class JetBlueTerminal(NewTerminalOperator):
    def __init__(self, terminal: Terminal):
        super().__init__(terminal)
        self.terminal = terminal
        self.airlines.append(self.curr_airline())
    def curr_airline(self) -> Airline: 
        return JetBlue()
    # def acceptable_airline(self, airline: Airline) -> bool: return airline.abbr() == "JB"


class TerminalFactory:
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    def __init__(self):
        self.terminals: list[Terminal] = list()

    def genTerminals(self, airport: Airport):
        """Called from the airport __init__ method."""
        # print("Called genTerminals")
        for i in range(Const.max_terminals):
            newTerminal: Terminal = Terminal(i)
            newTerminal.airport = airport
            self.terminals.append(newTerminal)
            airport.terminals.append(newTerminal)

    def createTerminal(self, airport: Airport) -> Terminal:
        newTerminal: Terminal = Terminal()
        newTerminal.airport = airport

#endregion


#region Flight

class Flight:
    """Class for representation of a flight.  Handles tracking passengers 
    on flight, executing the flight, setting the airline, & tracking vital 
    information about the flight."""
    MAX_PASSENGERS: int = Const.max_passengers
    def __init__(self, origin: Airport, destination: Airport, week: int, day: str):
        self.plane: Airplane = None
        self.airline: Airline = None
        # self.set_airline()
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
        self.date: Date = None
        self.week: int = week
        self.day: str = day

        self.passengers: list[Passenger] = list()
        self.first_class_passengers: list[Passenger] = list()
        
    def execute_flight(self) -> bool:
        """Execute the flight.  Move plane, passengers from origin airport to destination airport."""
        if self.completed:
            msg: str = f"Error: Flight {self.name} has already been completed."
            print(msg)
            return False
        onTime: bool = True
        delays: int = 0

        # check for delays
        delay_prob: float = random.random()
        if self.plane.airline.delay_chance() >= delay_prob:
            onTime = False
            delays += 1
            print(f"Flight {self.name} was delayed by the Airline")
        
        # check for mechanical issues
        break_down_prob: float = random.random()
        if self.plane.manufacturer.break_down_prob() >= break_down_prob:
            onTime = False
            delays += 1
            print(f"Flight {self.name} was delayed by mechanical issues with the plane")

        # check for weather
        poor_weather_prob: float = random.random()
        if self.departure.poor_weather_prob >= poor_weather_prob: 
            onTime = False
            delays += 1
            print(f"Flight {self.name} was delayed due to poor weather")
        
        self.on_time = onTime
        if not onTime:
            if delays > 1:
                print(f"Flight {self.name} was delayed and canceled.")
                return False

        # allowed to execute the flight
        self.currLocation = self.arrival
        if self.num_passengers != 0:
            for traveler in self.passengers:
                if not traveler.ticket.is_valid():  # ticket is not valid
                    pass
                traveler.setLocation(self.arrival)

                # change location of plane from origin airport to arrival airport
                self.departure.removePlane(self.plane)
                self.arrival.addPlane(self.plane)
                self.plane.currentAirport = self.arrival
            """
            # self.departureTerminal.curr_flight = None
            # self.arrivalTerminal.curr_flight = None
            self.departureTerminal.departing_flight = None
            # self.arrivalTerminal.arriving_flight = self  # will this work?
            self.departureTerminal.arriving_flight = None
            self.arrivalTerminal.departing_flight = self
            """

        self.completed = True
        msg: str = f"Flight {self.name} tookoff from {self.departure.name} and landed in {self.arrival.name} with {self.num_passengers} passengers onboard."
        print(msg)
        return True

    def set_airline(self):
        """Method to set the airline of the flight. Called when the flight is scheduled."""
        if self.departure is None and self.arrival is None:
            return None

        # --- Create Airline ---
        # Get airlines that fly between origin and destination
        airlines: list[Airline] = [AmericanAirlines(), UnitedAirlines(), DeltaAirlines(), JetBlue()]
        available_airlines: list[Airline] = list()  # list of airlines that fly between origin and destination
        for i in range(len(airlines)):
            airline: Airline = airlines[i]
            if airline.flies_to(self.departure) and airline.flies_to(self.arrival):
                available_airlines.append(airline)

        # Assign airline to flight randomly
        self.airline = random.choice(available_airlines)

    @property
    def name(self) -> str:
        return f"{self.departure.getName()}_{self.arrival.getName()}_{self.airline.abbr()}_{self.flight_number}"

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
        return bool(self.num_first_class != self.plane.first_class_seats)
            
    @property
    def flight_number(self) -> int: return self._flight_number
    @flight_number.setter
    def flight_number(self, newNumber: int): self._flight_number = newNumber

    @property
    def flight_log(self) -> dict:
        log: dict = {
            'Week': self.week,
            'Day': self.day,
            'Airline': self.airline.name(),
            'Name': self.name,
            'Departure': self.departure.name,
            # 'Departure Terminal': self.departureTerminal.name or None,
            'Arrival': self.arrival.name,
            # 'Arrival Terminal': self.arrivalTerminal.name or None,
            'Plane': self.plane.name,
            'Aircraft Manufacturer': self.plane.manufacturer.name(),
            'Passengers': self.passengers.__len__(),
            'Passenger List': [traveler.name for traveler in self.passengers],
            'First Class Passengers': [traveler.name for traveler in self.first_class_passengers],
            'On Time': self.on_time,
            'Date': f"{self.day}-{self.week}",
            'Week': self.week,
            'DayOfWeek': self.day
        }
        return log

    def show_flight_info(self):
        msg: str = f"Flight {self.name} on {self.week}-{self.day}."
        return msg

class FlightFactory:
    """Factory to handle flight creation and accessing/searching specific 
    flights. Handles creating & assigning planes to flights as well as 
    setting airline of flight."""
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    num_flights: int = 0
    def __init__(self):
        self.flight_log: list[Flight] = list()  # list of scheduled flights
        self.airplaneFactory = AirplaneFactory()

    def assign_plane_to_flight(self, flight: Flight):#, week: int, day: str):
        """Method to assign a plane for a flight."""
        origin: Airport = flight.departure
        week: int = flight.week
        day: str = flight.day
        # Set the Plane for the flight
        if week == 1 and day == 'Monday':
            # if simulation is in beginning then create the plane
            plane: Airplane = self.airplaneFactory.createAirplane(flight.airline)
        else:
            plane: Airplane = None
            # get planes at airport that are used by airline
            airline_planes = origin.get_planes_by_airline(flight.airline)
            
            # get planes that have a flight already assigned
            scheduled_flights_planes: list[Airplane] = []  # list of unavailable planes
            for scheduled_flight in self.flight_log:
                # check scheduled_flight is from the same airport as the new flight
                if scheduled_flight.departure == flight.departure and scheduled_flight.week == week and scheduled_flight.day == day:
                    scheduled_flights_planes.append(scheduled_flight.plane)
            
            # loop through planes the airline has at the origin
            for currPlane in airline_planes:
                if currPlane not in scheduled_flights_planes:
                    # if the current plane is not assigned a flight yet
                    plane = currPlane
            
            if plane is None:
                # print("No plane available, must create new one")
                # no available planes, airline must find plane for flight
                plane: Airplane = self.airplaneFactory.createAirplane(flight.airline)

        plane.currentAirport = origin  # set plane's current location to the origin airport
        flight.plane = plane  # assign the flight a plane
        origin.planes.append(plane)  # the plane is located at the origin airport until the flight takes off

    @staticmethod
    def get_available_terminals(flight_type: str, airport: Airport, airline: Airline=None) -> 'list[Terminal]':
        """Static method to get open terminals for a specific airline at an 
        airport. If an airline is not specified, it will return any open 
        terminals at the airport."""
        terminals: list[Terminal] = list()
        for terminal in airport.terminals:
            if flight_type == 'arrival':
                if terminal.arrival_available():
                    terminals.append(terminal)
            elif flight_type == 'departure':
                if terminal.departure_available():
                    terminals.append(terminal)
        
        avail = terminal.arrival_available() if flight_type == 'arrival' else terminal.departure_available()

        # print("HERE", len(terminals), airport, airline, [terminal.name for terminal in terminals])
        print("HERE", airport, flight_type,
              terminal.acceptable_airline(airline), 
            #   terminal.is_available(), 
              avail,
              airline, 
              [terminal.name for terminal in terminals])
        return terminals

    def assign_flight_terminals(self, flight: Flight, origin: Airport, destination: Airport):
        """Method that will assign arrival and departure terminals to the flight.
        NOTE: Here the flights haven't taken off yet so we are setting the 
        originTerminal as the departing_flight and the destinatinoTerminal as 
        the arriving_flight
        Remember: flight.departureTerminal is to originTerminal as flight.arrivalTerminal is to destinationTerminal
        """
        originTerminal: Terminal = None  # departing_flight
        destinationTerminal: Terminal = None  # arriving_flight
        airline: Airline = flight.airline
        # get the open terminals at each airport
        open_origin_terminals: list[Terminal] = self.get_available_terminals('arrival', origin)#, airline)
        open_destination_terminals: list[Terminal] = self.get_available_terminals('departure', destination)#, airline)
        assert len(open_origin_terminals) != 0
        assert len(open_destination_terminals) != 0

        for terminal in origin.terminals:
            # check that terminal is available 
            if terminal in open_origin_terminals:
                # we will dock the flight to the terminal now
                originTerminal = terminal
                # here the terminal could belong to any airline so we need to check/set airline
                if airline not in originTerminal.airlines:
                    # terminal hasn't encountered airline yet
                    if isinstance(airline, AmericanAirlines):
                        originTerminal = AmericanAirlinesTerminal(originTerminal)
                    elif isinstance(airline, UnitedAirlines):
                        originTerminal = UnitedAirlinesTerminal(originTerminal)
                    elif isinstance(airline, DeltaAirlines):
                        originTerminal = DeltaAirlinesTerminal(originTerminal)
                    elif isinstance(airline, JetBlue):
                        originTerminal = JetBlueTerminal(originTerminal)
                # set the flight with the terminal
                originTerminal.departing_flight = flight
                break
        for terminal in destination.terminals:
            # check that terminal is available
            if terminal in open_destination_terminals:
                # we will dock the flight to the terminal now
                destinationTerminal = terminal
                # here the terminal could belong to any airline so we need to check/set airline
                if airline in terminal.airlines:
                    if isinstance(airline, AmericanAirlines):
                        destinationTerminal = AmericanAirlinesTerminal(destinationTerminal)
                    elif isinstance(airline, UnitedAirlines):
                        destinationTerminal = UnitedAirlinesTerminal(destinationTerminal)
                    elif isinstance(airline, DeltaAirlines):
                        destinationTerminal = DeltaAirlinesTerminal(destinationTerminal)
                    elif isinstance(airline, JetBlue):
                        destinationTerminal = JetBlueTerminal(destinationTerminal)
                # set the flight with the terminal
                destinationTerminal.arriving_flight = flight
                break
        # assign flight terminals
        flight.departureTerminal = originTerminal
        flight.arrivalTerminal = destinationTerminal
        print(flight, flight.departureTerminal, originTerminal, flight.arrivalTerminal, destinationTerminal)

        # ALL OLD BELOW
        return 

        for terminal in origin.terminals:
            # check that terminal is applicable with flight airline
            if terminal in open_origin_terminals:
                print("HEREE")
                # here the terminal could belong to any airline
                if len(terminal.airlines) == 0:
                    # no airline set at terminal yet
                    print(f"No airline set at terminal {terminal} for flight {flight}")
                    if isinstance(airline, AmericanAirlines):
                        originTerminal = AmericanAirlinesTerminal(terminal)
                    elif isinstance(airline, UnitedAirlines):
                        originTerminal = UnitedAirlinesTerminal(terminal)
                    elif isinstance(airline, DeltaAirlines):
                        originTerminal = DeltaAirlinesTerminal(terminal)
                    elif isinstance(airline, JetBlue):
                        originTerminal = JetBlueTerminal(terminal)
                    originTerminal.airport = origin
                    originTerminal.curr_flight = flight
                else:
                    # terminal has at least 1 airline set
                    if airline in terminal.airlines:
                        originTerminal.airport = origin
                        # originTerminal.curr
                        originTerminal.departing_flight = flight
                    else:
                        # terminal hasn't encountered airline yet
                        if isinstance(airline, AmericanAirlines):
                            originTerminal = AmericanAirlinesTerminal(terminal)
                        elif isinstance(airline, UnitedAirlines):
                            originTerminal = UnitedAirlinesTerminal(terminal)
                        elif isinstance(airline, DeltaAirlines):
                            originTerminal = DeltaAirlinesTerminal(terminal)
                        elif isinstance(airline, JetBlue):
                            originTerminal = JetBlueTerminal(terminal)

                terminal.airport = origin
                terminal.curr_flight = flight
                originTerminal = terminal
                break
        
        for terminal in destination.terminals:
            # check that terminal is applicable with flight airline
            if terminal in open_destination_terminals:
                terminal.airport = destination
                terminal.curr_flight = flight
                destinationTerminal = terminal
                break
        
        # check originTerminal and destinationTerminal were both found
        if originTerminal is None:
            open_terminals: list[Terminal] = self.get_available_terminals(origin)
            if len(open_terminals) != 0:
                # check if terminal hasn't been assigned an airline yet 
                # (i.e the terminal hasn't been used yet)
                open_terminals[0].curr_flight = flight
                # if len(open_terminals[0].airlines) == 0:
                    # open_terminals[0].airlines.append()
                # origin airport does not have any open terminals for this airline
                if isinstance(airline, AmericanAirlines):
                    originTerminal = AmericanAirlinesTerminal(open_terminals[0])
                elif isinstance(airline, UnitedAirlines):
                    originTerminal = UnitedAirlinesTerminal(open_terminals[0])
                elif isinstance(airline, DeltaAirlines):
                    originTerminal = DeltaAirlinesTerminal(open_terminals[0])
                elif isinstance(airline, JetBlue):
                    originTerminal = JetBlueTerminal(open_terminals[0])
                originTerminal.airport = origin
                originTerminal.curr_flight = flight
            else:
                print(f"An open terminal could not be found at {origin.name}")
        if destinationTerminal is None:
            open_terminals: list[Terminal] = self.get_available_terminals(destination)
            if len(open_terminals) != 0:
                # destination airport does not have any open terminals for this airline
                if isinstance(airline, AmericanAirlines):
                    destinationTerminal = AmericanAirlinesTerminal(open_terminals[0])
                elif isinstance(airline, UnitedAirlines):
                    destinationTerminal = UnitedAirlinesTerminal(open_terminals[0])
                elif isinstance(airline, DeltaAirlines):
                    destinationTerminal = DeltaAirlinesTerminal(open_terminals[0])
                elif isinstance(airline, JetBlue):
                    destinationTerminal = JetBlueTerminal(open_terminals[0])
                destinationTerminal.airport = destination
                destinationTerminal.curr_flight = flight
            else:
                print(f"An open terminal could not be found at {destination.name}")

        # assign flight terminals
        flight.departureTerminal = originTerminal
        flight.arrivalTerminal = destinationTerminal

    def assign_flight_terminals2(self, flight: Flight):
        origin: Airport = flight.departure
        destination: Airport = flight.arrival
        originTerminal: Terminal = None
        destinationTerminal: Terminal = None
        airline: Airline = flight.airline
        # get the open terminals at each airport
        open_origin_terminals: list[Terminal] = self.get_available_terminals('arrival', origin)#, airline)
        open_destination_terminals: list[Terminal] = self.get_available_terminals('departure', destination)#, airline)
        # assert len(open_origin_terminals) != 0
        # assert len(open_destination_terminals) != 0

        # 1. get single open terminal in origin airport
        for terminal in origin.terminals:
            # if terminal in open_origin_terminals:
            # if terminal.departure_available():
            if terminal.departing_flight == None:
                # found open terminal
                originTerminal = terminal
                break

        originTerminal.departing_flight = flight  # nonetype object has no attribute 'departing_flight'
        flight.departureTerminal = originTerminal

        # the originTerminal could belong to any airline so we need to check/set airline
        if airline not in originTerminal.airlines:
            # terminal hasn't encountered airline yet
            if isinstance(airline, AmericanAirlines):
                originTerminal = AmericanAirlinesTerminal(originTerminal)
            elif isinstance(airline, UnitedAirlines):
                originTerminal = UnitedAirlinesTerminal(originTerminal)
            elif isinstance(airline, DeltaAirlines):
                originTerminal = DeltaAirlinesTerminal(originTerminal)
            elif isinstance(airline, JetBlue):
                originTerminal = JetBlueTerminal(originTerminal)
                

        # 2. get single open terminal in destination airport
        for terminal in destination.terminals:
            # if terminal in open_destination_terminals:
            # if terminal.arrival_available():
            if terminal.arriving_flight == None:
                # found open terminal
                destinationTerminal = terminal
                break
        
        destinationTerminal.arriving_flight = flight  # nonetype object has no attribute 'arriving_flight'
        flight.arrivalTerminal = destinationTerminal

        # the destinationTerminal could belong to any airline so we need to check/set airline
        if airline not in destinationTerminal.airlines:
            # terminal hasn't encountered airline yet
            if isinstance(airline, AmericanAirlines):
                destinationTerminal = AmericanAirlinesTerminal(destinationTerminal)
            elif isinstance(airline, UnitedAirlines):
                destinationTerminal = UnitedAirlinesTerminal(destinationTerminal)
            elif isinstance(airline, DeltaAirlines):
                destinationTerminal = DeltaAirlinesTerminal(destinationTerminal)
            elif isinstance(airline, JetBlue):
                destinationTerminal = JetBlueTerminal(destinationTerminal)

    def createFlight(self, origin: Airport or str, destination: Airport or str, week: int=None, day: str=None) -> Flight:
        """Method to create a flight object."""
        flight: Flight = Flight(origin, destination, week, day)

        flight.set_airline()  # set the flight's airline
        # print(flight.airline)

        self.assign_plane_to_flight(flight)#, week, day)  # 

        # assign plane to terminal in origin and destination airport
        # self.assign_flight_terminals(flight, origin, destination)
        # self.assign_flight_terminals2(flight)

        flight.flight_number = FlightFactory.num_flights
        self.flight_log.append(flight)
        FlightFactory.num_flights += 1
        msg: str = f"Scheduled flight {flight.name} on plane {flight.plane.name} on {flight.week}-{flight.day}."
        # msg += f"({flight.departureTerminal} --> {flight.arrivalTerminal})"
        # msg += '\n'
        print(msg)
        return flight

    # --- Utility methods ---
    def getFlightsByDate(self, week: int=None, day: str=None) -> 'list[Flight]':
        flights: list[Flight] = list()
        for flight in self.flight_log:
            if flight.week == week and flight.day == day:
                flights.append(flight)
            elif flight.week == week and day is None:
                if flight.week == week:
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

#endregion


#region Ticket

class Ticket:
    """Ticket class to track a passenger's spot on a flight. Tracks all 
    relevant information the passenger would need to know about a flight."""
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
            # 'Departure Terminal': self.flight.departureTerminal.name or None,
            'Arrival': self.destination.getName(),
            # 'Arrival Terminal': self.flight.arrivalTerminal.name or None,
            'Flight Number': self.flight.flight_number,
            'Airline': self.airline.name(),
            'First Class': self.first_class,
            'Date': f"{self.day}-{self.week}",
            'Week': self.week,
            'DayOfWeek': self.day,
            'TicketID': self.ticket_id
        }
        return log

    def is_first_class(self) -> bool: 
        """Check if ticket is a first class ticket."""
        if self.traveler.is_team():
            return False
        return self.first_class

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
    """Decorator method base abstract class for tickets"""
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def is_first_class(self) -> bool: pass
    @abc.abstractmethod
    def is_valid(self) -> bool: pass

class FirstClassTicket(TicketDecorator):
    """Decorator method for creating a FirstClassTicket out of a normal Ticket."""
    def __init__(self, ticket: Ticket):
        super().__init__(flight=ticket.flight, traveler=ticket.traveler)
        self.first_class: bool = True

    def is_first_class(self) -> bool: return True

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
    """Factory for creating passenger's tickets for a flight."""
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
        """Method for creating a new passenger ticket.

        Args:
            flight (Flight): flight object of the ticket's flight
            traveler (Passenger): the person the ticket is assigned to
            first_class (bool, optional): determine if new ticket needs to be first class. Defaults to False.

        Returns:
            Ticket: new ticket object for the passenger & flight.
        """
        newTicket: Ticket = Ticket(flight, traveler)
        if first_class:
            # to get here flight.first_class_available() must  be true
            newTicket = FirstClassTicket(newTicket)  # Decorator method
            flight.first_class_passengers.append(traveler)
            flight.num_first_class += 1
        return newTicket
    

#endregion


#region Logger

class Logger:
    """Subject aka Observable or Publisher. Part of observer pattern"""
    def __init__(self, filename: str):
        self.filename: str = filename

    def write_to_file(self, newLog: dict):
        """Opens and reads a JSON file and adds the dictionary to the file."""
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
    def update(self, log): raise NotImplementedError

class FlightLogger(Logger):
    """FlightLogger for externally keeping track of flights. Updated after flight has executed."""
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    def __init__(self):
        super().__init__(filename='FlightLog.json')
        self.observers: list[Observer] = []  # list of instances using the FlightLogger
        self.flight_log: list[Flight] = []
    
    def register_observer(self, observer: Observer): self.observers.append(observer)
    def   remove_observer(self, observer: Observer): self.observers.remove(observer)

    def notify_observers(self): 
        for observer in self.observers:
            observer.update(self.flight_log)
    
    def condition_changed(self):
        currFlight: Flight = self.flight_log[-1]
        self.write_to_file(currFlight.flight_log)
        self.notify_observers()

    def update(self, newFlight: Flight):
        self.flight_log.append(newFlight)
        self.condition_changed()

class TicketLogger(Logger):
    """TicketLogger for externally keeping track of all tickets once they are created."""
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    def __init__(self):
        super().__init__(filename='TicketLog.json')
        self.observers: list[Observer] = []  # list of instances using the TicketLogger
        self.ticket_log: list[Ticket] = []
    
    def register_observer(self, observer: Observer): self.observers.append(observer)
    def   remove_observer(self, observer: Observer): self.observers.remove(observer)
    
    def notify_observers(self): 
        for observer in self.observers:
            observer.update(self.ticket_log)

    def condition_changed(self): 
        currTicket: Ticket = self.ticket_log[-1]
        self.write_to_file(currTicket.ticket_log)
        self.notify_observers()
    
    def update(self, newTicket: Ticket):
        self.ticket_log.append(newTicket)
        self.condition_changed()

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

        self.passengerFactory = PassengerFactory(amount=Const.max_travelers)  # 100
        self.airportFactory = AirportFactory()
        self.flightFactory = FlightFactory()
        self.ticketFactory = TicketFactory()
        
        self.airports: list[Airport] = self.airportFactory.getAirports()
        self.passengers: list[Passenger] = list()
        self.all_flights: list[Flight] = list()
        self.HUB_AIRPORT: Airport = self.airportFactory.HUB_AIRPORT

        self.master_schedule: list[Flight] = list()

        # create terminals
        # self.createTerminals()
        # create passengers
        self.createPassengers()

    def createTerminals(self):
        for airport in self.airports:
            self.terminalFactory.genTerminals(airport)
            # print(airport, airport.terminals)
    
    def createPassengers(self):
        msg: str = "> Creating passengers...."
        print(msg)
        for i in range(self.passengerFactory.max_passengers):
            new_passenger: Passenger = self.passengerFactory.createPassenger()
            self.passengers.append(new_passenger)
    
    def show_passengers(self):
        print('i \tName \tLocation \tHome Airport')
        for i, traveler in enumerate(self.passengers):
            print(i, traveler.name, traveler.currLocation, traveler.home_airport)

    @property
    def allow_remote_booking(self) -> bool:
        """Whether to allow passengers to book a flight when they aren't at the departure airport."""
        return True

    def schedule_day(self, week: int, day: str):
        """Method to schedule a day's worth of flights at all airports."""
        low_chance: int = 5  # the higher this number the better(?) the chance of an extra flight
        high_chance: int = 90  # the higher this number the better the chance an extra flight will be scheduled
        d_t_a: float = random.randint(low_chance, high_chance) / 100
        a_t_d: float = random.randint(low_chance, high_chance) / 100

        # loop through airports
        for i in range(len(self.airports)):
            airport: Airport = self.airports[i]
            if airport.is_hub_airport:  # not hub airport
                continue
            flight: Flight = None

            # ----- add daily flights in  -----
            origin: Airport = self.airportFactory.HUB_AIRPORT
            dest: Airport = airport
            for i in range(airport.per_day_in):
                flight = self.flightFactory.createFlight(origin=origin, destination=dest, week=week, day=day)
                self.master_schedule.append(flight)
            # add random chances of each airport getting extra flights 
            if airport.fly_chance_to >= d_t_a:
                flight = self.flightFactory.createFlight(origin=origin, destination=dest, week=week, day=day)
                self.master_schedule.append(flight)

            # ----- add daily flights out -----
            origin: Airport = airport
            dest: Airport = self.airportFactory.HUB_AIRPORT
            for i in range(airport.per_day_out):
                flight = self.flightFactory.createFlight(origin=origin, destination=dest, week=week, day=day)
                self.master_schedule.append(flight)
            # add random chances of each airport getting extra flights 
            if airport.fly_chance_from >= a_t_d:
                flight = self.flightFactory.createFlight(origin=origin, destination=dest, week=week, day=day)
                self.master_schedule.append(flight)
        msg: str = f"All flights scheduled for {day}, week {week}"
        print(msg)

    def book_flight(self, traveler: Passenger, origin: Airport, dest: Airport, day: str, week: int, confirm_msg: bool=False) -> bool:
        """Method to book a flight for a passenger. Returns whether passenger 
        was successfully able to book spot on flight."""
        if origin == dest:  # can't book flight to and from same airport
            msg: str = f"Error: Can't book flight to and from same airport {origin} -> {dest}."
            print(msg)
            return False

        if not self.allow_remote_booking:
            if traveler.currLocation == origin:
                msg: str = "Error: You cannot book a flight"
                print(msg)

        # get the flight object
        # NOTE: Just to speed up the loop below
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
                if (not traveler.is_team()) and flight.first_class_available() and traveler.first_class_freq >= random.random():  # First Class Ticket
                    # print(traveler.name, 'is a first class passenger')
                    ticket = self.ticketFactory.createTicket(flight, traveler, first_class=True)
                else:  # Economy Ticket
                    ticket = self.ticketFactory.createTicket(flight, traveler, first_class=False)
                traveler.ticket = ticket  # give the traveler their ticket
                self.ticketLog.update(ticket)

                # 4. add traveler to flight
                flight.add_passenger(traveler)
                traveler.flight = flight  # set the travelers flight to the current on one
                if confirm_msg:
                    msg: str = f"Successfully booked ticket from {origin} to {dest} for {traveler} on flight {flight.name}"
                    print(msg)
                return True
        if confirm_msg:
            msg: str = f"Error({len(flight_lst)}): A flight from {origin} to {dest} on {week}-{day} is not available for {traveler}."
            print(msg)
        return False

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
    
#endregion


#region Simulator
class Simulator:
    """Simulator class to handle events not related to specific features 
    of the AirTrafficControl or other features specific to flying/airports.
    """
    def __new__(cls, *args, **kwds):
        """Singleton Implementation"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it
    
    def __init__(self, weeks: int=Const.numWeeks):
        self.__num_weeks: int = weeks  # number of weeks to run the simulation
        self.dayCount: int = 1
        self.currWeek: int = 1
        self.date: Date = Date()
        self.flightLog: FlightLogger = FlightLogger()
        self.ticketLog: TicketLogger = TicketLogger()
        self.user: Passenger = None
        self.atc: AirTrafficControl = AirTrafficControl(self.flightLog, self.ticketLog)

    @property
    def FINAL_WEEK(self) -> int: return self.__num_weeks

    def make_user(self):
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
        self.user = user

    def get_option(self, day: Date.dayOfWeek):
        if self.user is None:
            self.make_user()
        user = self.user

        print(f"Current location: {user.currLocation.getName()}")
        print(f"Current Day: {day}, Week {self.currWeek}, Day {self.dayCount}")

        # show available flights
        print("Available Flights: ")
        available_flights: list[Flight] = self.atc.flightFactory.getFlightByOrigin(user.currLocation, self.currWeek, day)
        for i, flight in enumerate(available_flights, start=1):
            print(f"{i}. {flight.show_flight_info()}")
        choice: int = int(input("Which number flight would you like to choose? "))
        usr_flight: Flight = available_flights[choice]

        origin: Airport = usr_flight.departure
        dest: Airport = usr_flight.arrival
        flight: Flight = self.atc.book_flight(passenger_name=user.name, origin=origin, dest=dest, day=day, week=self.currWeek, confirm_msg=True)
        
    def run_simulation(self, usr_inpt: bool=False):
        print("<<<<< New Simulation >>>>>")
        # Show current parameters for simulation
        print(f"Number of weeks: {Const.numWeeks}")
        print(f"Number of travelers: {Const.max_travelers}")
        print(f"Max Capacity per plane: {Const.max_passengers}")
        # iterate through weeks until final week is reached
        while self.currWeek <= self.FINAL_WEEK:
            print(f"********** Week {self.currWeek} **********")

            # iterate through the days of the week
            for day in Date.WEEK:
                self.update()
                print('\n')
                
                self.schedule_new_day(day)  # schedule a day of flights
                
                if usr_inpt:
                    self.get_option(day)
                
                self.book_new_day(day)  # book passengers on flights
                
                self.execute_day(day)  # flights fly passengers to destination
                
                # self.update()
                print('\n')
                Date().new_day()

            self.end_week()
            print("\n\n")
        self.end_simulation()

    def end_simulation(self): print("<<<<< End Simulation >>>>>")

    def update(self):
        airport_pass = {}
        for airport in self.atc.airports:
            airport_pass[airport] = {'Passengers': [], 'Planes': []}

        for traveler in self.atc.passengers:
            loc: Airport = traveler.currLocation
            airport_pass[loc]['Passengers'].append(traveler.name)

        print("Locations of travelers.")
        for ap, travelers in airport_pass.items():
            print(ap, len(travelers['Passengers']), travelers['Passengers'])

    def end_week(self):
        print(f"********** End Week {self.currWeek} **********")
        print(f"Number of airplanes: {self.atc.flightFactory.airplaneFactory.num_planes}")
        self.update()
        # Date().new_day()
        self.currWeek += 1

    def schedule_new_day(self, day: str):
        print(f"***** {day} *****")
        print("Scheduling flights....")
        self.atc.schedule_day(self.currWeek, day)
        # self.dayCount += 1

    def go_home(self, day: str):
        """Commands for all travelers to book flights to their home airports."""
        for traveler in self.atc.passengers:
            home_ap: Airport = traveler.home_airport
            if home_ap == traveler.currLocation:
                continue
            else:
                origin: Airport = traveler.currLocation
                dest: Airport = home_ap

                success: bool = self.atc.book_flight(
                    passenger_name=traveler.name, 
                    # origin=traveler.currLocation.getName(), 
                    # dest=ap.getName(), 
                    origin=origin,
                    dest=dest,
                    day=day, 
                    week=self.currWeek, 
                    confirm_msg=True
                )

    def book_new_day(self, day: str):
        """Perform operations necessary for booking the passengers flights."""
        print(f"---------- Booking [{day}] ----------")
        for traveler in self.atc.passengers:
            if traveler.currLocation.getName() == 'DIA':  # DIA -> ___
                origin: Airport = self.atc.airportFactory.HUB_AIRPORT
                dest: Airport = self.atc.airportFactory.randomAirport(inc_hub=False)
            else:  # ___ -> DIA
                origin: Airport = traveler.currLocation
                dest: Airport = self.atc.airportFactory.HUB_AIRPORT

            success: bool = self.atc.book_flight(
                traveler=traveler,
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
            self.flightLog.update(flight)
        print(f"===== Finished Executing {day} =====")

#endregion



if __name__ == "__main__":
    # File is run from command line.
    # Save the simulation output to the SimResults file.
    sim: Simulator = Simulator()

    original_stdout = sys.stdout  # Save a reference to the original standard output
    with open('SimResults.txt', 'w') as file:
        sys.stdout = file  # Change the standard output to SimResults.txt
        sim.run_simulation(False)
        sys.stdout = original_stdout  # Reset the standard output to its original value

else:  # Imported as a Module
    pass
