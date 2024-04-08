INSERT INTO Room (RoomNumber) VALUES (1),(2),(3),(4),(5);

INSERT INTO Trainer (TrainerEmail, FirstName, LastName) VALUES
('bill@gates.com', 'Bill', 'Gates'),
('steve@jobs.com', 'Steve', 'Jobs'),
('john@doe.com', 'John', 'Doe'),
('jane@zoe.com', 'Jane', 'Zoe'),
('robert@wood.com', 'Robert', 'Wood');

INSERT INTO ClubMember (MemberEmail, FirstName, LastName, PhoneNumber, Address, Weight, Height, Age, Sex, DesiredWeight, DailyTime, WarmupTime, PushupReps, SitupReps, SquatReps, WeightReps, TreadmillMin, CooldownTime, TotalMinutes, TotalCalories, TotalDays) VALUES
('walter@levine.com', 'Walter', 'Levine', '613-421-1475', '1241 Main Street', 142, 135, 25, 'Male', 100, 100, 5, 20, 20, 20, 20, 20, 5, 50000, 80000, 700),
('todd@stevens.com', 'Todd', 'Stevens', '613-123-2233', '242 North Street', 180, 70, 50, 'Male', 150, 200, 7, 20, 25, 25, 20, 25, 7, 52450, 72200, 500),
('james@crossman.com', 'James', 'Crossman', '613-352-4852', '555 South Street', 200, 18, 25, 'Male', 120, 150, 5, 10, 10, 0, 10, 20, 5, 30000, 50055, 200),
('mary@rowles.com', 'Mary', 'Rowles', '613-745-3486', '1023 Main Avenue', 70, 200, 26, 'Female', 50, 125, 5, 30, 30, 30, 30, 30, 5, 59000, 87700, 755),
('betty@boyle.com', 'Betty', 'Boyle', '613-952-0242', '6542 Main Street', 150, 175, 38, 'Female', 120, 30, 5, 15, 10, 20, 20, 10, 5, 40000, 50100, 612);

INSERT INTO Achievements (MemberEmail, AchievementName, DateEarned) VALUES
('walter@levine.com', 'Signed Up!', '2019-04-11'),
('todd@stevens.com', 'Signed Up!', '2018-05-12'),
('james@crossman.com', 'Signed Up!', '2020-12-20'),
('mary@rowles.com', 'Signed Up!', '2017-01-05'),
('betty@boyle.com', 'Signed Up!', '2019-09-15'),
('betty@boyle.com', '600 Days Attended!', '2022-09-15'),
('walter@levine.com', '600 Days Attended!', '2022-01-22'),
('mary@rowles.com', '600 Days Attended!', '2022-04-01');

INSERT INTO Equipment (EquipName, LastMaintained, RoomNumber) VALUES
('Dumbell', '2022-05-06', 1),
('Dumbell', '2022-02-18', 2),
('Dumbell', '2022-05-20', 3),
('Treadmill', '2022-08-11', 4),
('Treadmill', '2022-01-25', 1),
('Treadmill', '2021-05-07', 2),
('Punching Bag', '2021-12-17', 3);

INSERT INTO GroupClasses (DateBooked, TrainerEmail, RoomNumber) VALUES
('2024-10-22', 'john@doe.com', 4),
('2024-05-11', 'bill@gates.com', 3); 

INSERT INTO TrainingSessions (DateBooked, TrainerEmail, RoomNumber, MemberEmail) VALUES
('2024-09-15', 'john@doe.com', 1, 'betty@boyle.com'),
('2024-05-24', 'bill@gates.com', 2, 'james@crossman.com'),
('2024-05-24', 'steve@jobs.com', 3, 'todd@stevens.com');

INSERT INTO AdminStaff (AdminEmail, FirstName, LastName) VALUES
('larry@staff.com', 'Larry', 'Lu'),
('barry@staff.com', 'Barry', 'Buu');

INSERT INTO PartakesIn (GroupID, MemberEmail) VALUES
(1, 'walter@levine.com'),
(1, 'todd@stevens.com'),
(1, 'james@crossman.com'),
(2, 'mary@rowles.com'),
(2, 'betty@boyle.com');

INSERT INTO Bill (Amount, MemberEmail, DatePaid) VALUES 
(90, 'betty@boyle.com', '2023-01-22'),
(110, 'todd@stevens.com', '2023-02-22'),
(50, 'todd@stevens.com', '2022-02-10'),
(50, 'walter@levine.com', '2022-04-14'),
(70, 'james@crossman.com', '2023-05-24'),
(70, 'mary@rowles.com', '2023-12-10');

INSERT INTO AvailableDates (TrainerEmail, AvailableDate) VALUES
('bill@gates.com', '2024-04-02'),
('bill@gates.com', '2024-04-03'),
('bill@gates.com', '2024-04-04'),
('bill@gates.com', '2024-04-05'),
('bill@gates.com', '2024-04-08'),
('bill@gates.com', '2024-04-09'),
('bill@gates.com', '2024-04-11'),
('bill@gates.com', '2024-04-12'),
('bill@gates.com', '2024-04-17'),
('bill@gates.com', '2024-04-18'),
('bill@gates.com', '2024-04-19'),
('bill@gates.com', '2024-04-24'),
('bill@gates.com', '2024-04-25'),
('steve@jobs.com', '2024-04-02'),
('steve@jobs.com', '2024-04-03'),
('steve@jobs.com', '2024-04-04'),
('steve@jobs.com', '2024-04-05'),
('steve@jobs.com', '2024-04-06'),
('steve@jobs.com', '2024-04-07'),
('steve@jobs.com', '2024-04-11'),
('steve@jobs.com', '2024-04-12'),
('steve@jobs.com', '2024-04-13'),
('steve@jobs.com', '2024-04-14'),
('steve@jobs.com', '2024-04-15'),
('steve@jobs.com', '2024-04-24'),
('steve@jobs.com', '2024-04-25'),
('john@doe.com', '2024-04-02'),
('john@doe.com', '2024-04-03'),
('john@doe.com', '2024-04-05'),
('john@doe.com', '2024-04-06'),
('john@doe.com', '2024-04-07'),
('john@doe.com', '2024-04-08'),
('john@doe.com', '2024-04-09'),
('john@doe.com', '2024-04-10'),
('john@doe.com', '2024-04-15'),
('john@doe.com', '2024-04-16'),
('john@doe.com', '2024-04-23'),
('john@doe.com', '2024-04-24'),
('john@doe.com', '2024-04-25'),
('jane@zoe.com', '2024-04-02'),
('jane@zoe.com', '2024-04-03'),
('jane@zoe.com', '2024-04-05'),
('jane@zoe.com', '2024-04-06'),
('jane@zoe.com', '2024-04-07'),
('jane@zoe.com', '2024-04-12'),
('jane@zoe.com', '2024-04-13'),
('jane@zoe.com', '2024-04-14'),
('jane@zoe.com', '2024-04-15'),
('jane@zoe.com', '2024-04-16'),
('jane@zoe.com', '2024-04-23'),
('jane@zoe.com', '2024-04-29'),
('jane@zoe.com', '2024-04-30'),
('robert@wood.com', '2024-04-02'),
('robert@wood.com', '2024-04-03'),
('robert@wood.com', '2024-04-05'),
('robert@wood.com', '2024-04-06'),
('robert@wood.com', '2024-04-07'),
('robert@wood.com', '2024-04-08'),
('robert@wood.com', '2024-04-09');
