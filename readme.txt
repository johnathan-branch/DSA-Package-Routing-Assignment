To execute navigate to the src directory, then run: python main.py

Program Overview
---

Scenario:

A parcel delivery service needs to determine an efficient route and delivery distribution for daily local deliveries because packages are not currently being consistently delivered by their promised deadlines. The local delivery route includes three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements listed in the attached Package File.

Your task is to determine an algorithm, write code, and present a solution where all 40 packages are delivered on time while meeting each package’s requirements and keeping the combined total distance traveled by all trucks under 140 miles. The delivery locations are shown on the attached Downtown Map, and distances between locations are provided in the attached Distance Table.

The intent is for the program to be usable not only for this specific city but also for many other cities. As such, you must include detailed comments to make the code easy to follow and to justify the design decisions made during development.

A supervisor must be able to view, at assigned points, the progress of each truck and its packages using any of the variables listed in the Package File, including delivery status and delivery time.


Assumptions:

Each truck can carry a maximum of 16 packages, and each package ID is unique.

Trucks travel at an average speed of 18 miles per hour and have an unlimited fuel supply.

There are no collisions.

Three trucks and two drivers are available. Each driver remains with the same truck while it is in service.

Drivers leave the hub no earlier than 8:00 a.m. with a fully loaded truck and may return to the hub to load additional packages if needed.

Delivery and loading times are instantaneous. These times are factored into the average truck speed.

Each package may have up to one special note.

The delivery address for package #9 (Third District Juvenile Court) is incorrect and will be corrected at 10:20 a.m. The correct address (410 S. State St., Salt Lake City, UT 84111) is not known until that time.

Distances provided in the Distance Table are symmetric (the same in both directions).

The day ends when all 40 packages have been delivered.