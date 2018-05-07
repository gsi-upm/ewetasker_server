# EWE Tasker Server

This repository contains EWE Tasker Server module, written in Golang.

## API CALLS

| Route | Method | Description |
|---|---|---|
| /channels  | GET  | Get a list of base channels available at the platform  |
| /channels/user/{userID}  | GET  |  Get a list of channels available for the specified user |
| /channels/place/{placeID}  | GET  | Get a list of channels available at the platform associated to a certain place |
| /rules  | GET  | Get a list of rules available at the platform  |
| /rules/user/{userID}  | GET  | Get a list of rules available at the platform for the specified user |
| /rules/place/{placeID}  | GET  | Get a list of rules available at the platform associated to a certain place |