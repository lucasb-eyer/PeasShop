conn = 0

connect = ->
    if not window["WebSocket"]?
        err = "No WebSocket support. Get a better browser!"
        alert err
        throw new Error err

    # Extract the game ID from the current location.
    g = (window.location.pathname.match /.*game\/([a-zA-Z0-9]+).*/)[1]

    # And make a websocket connection accordingly
    addr = "ws://#{window.location.host}/ws?g=#{g}"
    conn = new WebSocket addr

    conn.onopen = (evt) ->
        conn.send g

    conn.onclose = (evt) ->
        console.log "Connection lost"
        console.log evt

    conn.onmessage = (evt) ->
        console.log "Message!"
        console.log evt.data
        msg = JSON.parse evt.data
        switch msg.type
            when 'start'
                start_game msg.items

start_game = (items) ->
    ($ '#waiting').hide()
    ($ '#game').show()

    # Put stuff into the arena!
    for item in items
        $ ''
