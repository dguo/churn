# churn [![Build Status](https://travis-ci.org/dguo/churn.svg?branch=master)](https://travis-ci.org/dguo/churn)
CLI for keeping track of credit card activity (payments and reward redemptions)

## Installation
`$ pip install churn`

## Usage
`$ churn --help`

## Motivation
While I use [Mint](https://www.mint.com/) ([Personal
Capital](https://www.personalcapital.com/) is one alternative) to keep track of
my personal finances, I've always used a spreadsheet to record my credit card
reward redemptions and to calculate my rewards to payments rate. The purpose of
this tool is to replace that spreadsheet with a CLI backed by a
[SQLite](https://sqlite.org/) database.

The data must be manually entered for now, but automating the data retrieval is
a possible goal.

## Development
If you have [Docker](https://docs.docker.com/) running, you can run `$ ./dev
up` to bring up a development environment. From here, you should be able to run
`$ churn`. Any changes to the source code should immediately be reflected in
the development environment.

## License
MIT
