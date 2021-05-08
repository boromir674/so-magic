Why this library?
=================

So Magic main capability is to infer Self-Organising Map models out of structured data.

Practically speaking there is a lot of effort to converting raw data into the "structured format",
that is ready to be digested by the "learning" algorithm. So Magic facilitates this process (aka pre-processing),
providing with pre-built commands and also supporting user-made commands for performing common operations
on "raw" data.

Apart from the ability to train SOM models (using the "learning" algorithm) So Magic provides with hyper-parameter
tuning given intrinsic and user-made extrinsic evaluation criteria.

Another feature is the easy way to persist models parameters and/or model evaluation statistics.
The library provides serialization and deserialization supporting JSON format.
