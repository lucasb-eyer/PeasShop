conn = 0

W = 600
H = 400

idify = (s) -> s.replace /[^a-zA-Z0-9]/g, -> '_'

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
                    do (item, i) ->
                        $i = mkitem item, i
                        $arena.append $i

                        $i.click ->
                            console.log item
                            conn.send JSON.stringify({type: 'wanna', id: item.id})
            when 'you_took'
                $i = $ "#" + idify msg.item
                $i.stop()
                $i = $i.detach()
                $i.appendTo $ '#p2'
                $i.css 'margin-left': 0, 'margin-top': 0
                $i.addClass 'has'

                ($ '#myscore').text msg.score.toFixed 2
                ($ '#mymoney').text msg.money
                if msg.color_bonus
                    ($ '#mybonus').text " + #{msg.color_bonus} color bonus"
                else
                    ($ '#mybonus').text ""

                if msg.replaces
                    for [1..5]
                        $("#" + idify msg.replaces).remove()
            when 'other_took'
                $i = $ "#" + idify msg.item
                $i.stop()
                $i = $i.detach()
                $i.appendTo $ '#p1'
                $i.css 'margin-left': 0, 'margin-top': 0
                $i.addClass 'has'
                ($ '#otherscore').text msg.other_score.toFixed 2
                ($ '#othermoney').text msg.other_money
                if msg.other_color_bonus
                    ($ '#otherbonus').text " + #{msg.other_color_bonus} color bonus"
                else
                    ($ '#otherbonus').text ""

                if msg.replaces
                    for [1..5]
                        $("#" + idify(msg.replaces)).remove()
            when 'win'
                alert 'OMG YOU WON'
            when 'lose'
                alert 'LOSER'
        return

mkitem = (item, i) ->
    $i = $ Mustache.render item_template, item
    $i.hide()

    t = (1.1 - +item.speed)*10000

    $i.attr id: idify item.id
    $i.css
        'margin-left': 600
        'margin-top': (i % 2) * 200
    $i.delay(i*1000).show().animate {'margin-left': -200}, t, 'linear'
    return $i

item_template = """
<div class=item>
    <img src={{img_url}} />
</div>
"""
