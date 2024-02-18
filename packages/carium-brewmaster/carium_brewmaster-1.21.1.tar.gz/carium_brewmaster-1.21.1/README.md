# Brewmaster
Library/utility collection for custom job

Reference: [Brewmaster](https://dota2.gamepedia.com/Brewmaster)

This library is for use in custom-job environments as developed with the [cariumsdk](https://pypi.org/project/cariumsdk/).

## Installation

```
pip install carium-brewmaster
```

## Organization

Brewmaster APIs are organized based on the services and the objects that they are managing.
For example:

- caredb
  - action
  - article
  - challenge
  - org
    - appointment
    - contact
- overlord
  - interaction
    - profile
    - instance
