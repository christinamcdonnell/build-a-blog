# from post.html follows subject display
<div class="post-date">
    {{p.created.strftime("%b %d, %Y")}}
</div>

# from permalink.html was before {{subject}}

<input type="submit" value="blog! Homepage" href="/blog"/>

# from newpost.html was before label subject display

        <input type="submit" value="blog! Homepage" href="/blog"/>

# from ViewPostHandler right before the render
# update the post maybe ???   #retrieved_model_post_instance.subject = ???
#retrieved_model_post_instance.content = ???   #retrieved_model_post_instance.put()
