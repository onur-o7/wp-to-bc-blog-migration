import html

a = html.unescape("Hanging Moss Decor for Luxury Homes &#038; Businesses")

b = html.unescape("Hanging Moss Decor for Luxury Homes & Businesses")


print(a.lower())
print(b.lower())
print(a==b)