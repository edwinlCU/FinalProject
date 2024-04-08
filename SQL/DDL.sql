CREATE TABLE Room (
  RoomNumber INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE Trainer (
  TrainerEmail VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL
);

CREATE TABLE ClubMember (
  MemberEmail VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL,
  PhoneNumber VARCHAR(15),
  Address VARCHAR(255),
  Weight INTEGER,
  Height INTEGER,
  Age INTEGER,
  Sex VARCHAR(255),
  DesiredWeight VARCHAR(255),
  DailyTime VARCHAR(255),
  WarmupTime INTEGER DEFAULT 5,
  PushupReps INTEGER DEFAULT 20,
  SitupReps INTEGER DEFAULT 10,
  SquatReps INTEGER DEFAULT 15,
  WeightReps INTEGER DEFAULT 20,
  TreadmillMin INTEGER DEFAULT 15,
  CooldownTime INTEGER DEFAULT 5,
  TotalMinutes INTEGER DEFAULT 0,
  TotalCalories INTEGER DEFAULT 0,
  TotalDays INTEGER DEFAULT 0
);

CREATE TABLE Achievements (
  MemberEmail VARCHAR(255) NOT NULL REFERENCES ClubMember(MemberEmail),
  AchievementName VARCHAR(255) NOT NULL, 
  DateEarned DATE NOT NULL,
  CONSTRAINT PK_Achievements PRIMARY KEY (MemberEmail, AchievementName)
);

CREATE TABLE GroupClasses (
  GroupID SERIAL PRIMARY KEY,
  DateBooked DATE NOT NULL,
  TrainerEmail VARCHAR(255) NOT NULL REFERENCES Trainer(TrainerEmail),
  RoomNumber INTEGER REFERENCES Room(RoomNumber)
);

CREATE TABLE Bill (
  TransactionID SERIAL PRIMARY KEY,
  Amount INTEGER NOT NULL, 
  MemberEmail VARCHAR(255) NOT NULL REFERENCES ClubMember(MemberEmail),
  DatePaid DATE NOT NULL
);

CREATE TABLE PartakesIn (
  GroupID INTEGER REFERENCES GroupClasses(GroupID),
  MemberEmail VARCHAR(255) NOT NULL REFERENCES ClubMember(MemberEmail),
  CONSTRAINT PK_PartakesIn PRIMARY KEY (GroupID, MemberEmail)
);

CREATE TABLE Equipment (
  EquipID SERIAL PRIMARY KEY,
  EquipName VARCHAR(255) NOT NULL,
  LastMaintained DATE NOT NULL,
  RoomNumber INTEGER REFERENCES Room(RoomNumber)
);

CREATE TABLE TrainingSessions (
  TrainID SERIAL PRIMARY KEY,
  DateBooked DATE NOT NULL,
  TrainerEmail VARCHAR(255) NOT NULL REFERENCES Trainer(TrainerEmail),
  RoomNumber INTEGER REFERENCES Room(RoomNumber),
  MemberEmail VARCHAR(255) NOT NULL REFERENCES ClubMember(MemberEmail)
);

CREATE TABLE AdminStaff (
  AdminEmail VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL
);

CREATE TABLE AvailableDates (
  TrainerEmail VARCHAR(255) NOT NULL REFERENCES Trainer(TrainerEmail),
  AvailableDate DATE NOT NULL,
  CONSTRAINT PK_AvailableDates PRIMARY KEY (TrainerEmail, AvailableDate)
);