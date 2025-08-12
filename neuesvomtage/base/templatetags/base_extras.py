from django import template

register = template.Library()


@register.filter(name="chunks")
def chunks(iterable, chunk_size):
    if not hasattr(iterable, "__iter__"):
        # can't use "return" and "yield" in the same function
        yield iterable
    else:
        i = 0
        chunk = []
        for item in iterable:
            chunk.append(item)
            i += 1
            if not i % chunk_size:
                yield chunk
                chunk = []
        if chunk:
            # some items will remain which haven't been yielded yet,
            # unless len(iterable) is divisible by chunk_size
            yield chunk


@register.simple_tag
def entry_list(feed, q=None, limit=7):
    """
    Returns the last entries of a feed. These are filtered by q if q is not None
    """
    entries = feed.entry_set.all()
    if q is not None:
        entries = entries.filter(title__icontains=q)
    return entries.order_by("-created_at")[:limit]


@register.filter
def strip_schema_from_url(url):
    return url.split("://")[-1].replace("www.", "").strip("/")
