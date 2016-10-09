Routing execution
=================

Following is the pseudo code for the routing execution model::

    if routing is not enabled for the request (no middleware/no decorator)
        do nothing

    if there is no entry of request.path_info in Router.source
        do nothing

    if there are multiple entries, order by their rank (ascending order)
        for each router
            if there are no destinations
                continue with the loop
            if the condition is met then break the loop else continue
        if the for loop did not break
            do nothing

        pick a random destination w.r.t their weightage
        route to the destination based on the action defined

