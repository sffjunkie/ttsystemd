app:
    @{{pypm}} run python -m {{project}}

app-dev:
    @{{pypm}} run textual run --dev {{project}}.__main__

app-console:
    @{{pypm}} run textual console -x SYSTEM -x EVENT

app-console-event:
    @{{pypm}} run textual console -x SYSTEM
