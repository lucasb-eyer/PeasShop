conn = 0

W = 600
H = 400

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
                ($ '#waiting').hide()
                ($ '#game').show()

                $arena = $ '#arena'

                # Put stuff into the arena!
                for item, i in msg.items
                    $i = mkitem item, i
                    $arena.append $i

                    $i.click ->
                        console.log item
                        # TODO
                        # conn.send {''}
            when 'you_took'
            when 'other_took'
                ($ )

mkitem = (item, i) ->
    $i = $ Mustache.render item_template, item
    $i.hide()

    t = (1.1 - +item.speed)*10000

    $i.css
        'margin-left': 600
        'margin-top': (i % 2) * 200
    $i.delay(i*2000).show().animate {'margin-left': -200}, t, 'linear'
    return $i

item_template = """
<div class=item>
    <img src={{img_url}} />
</div>
"""
