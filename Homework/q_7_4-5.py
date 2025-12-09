print("My kitty cat likes %s\n" \
      "My kitty cat likes %s\n" \
      "My kitty cat fell on his %s\n" \
      "And now thinks he's a %s\n" \
        % ('roast beef','ham','head','clam'))

response={'salution':'Hello there',
          'name':'Ingram',
          'product':'babysitter',
          'verbed':'fallen',
          'room':'kichen',
          'animals':'dogs',
          'amount':'5000',
          'percent':'50',
          'spokesman':'Jason',
          'job_title':'producer'}

letter="""Dear {salution} {name},\n\
      Thank you for your letter.We are sorry thqt our {product}\
      {verbed} in your {room}. Please note that it should never\
      be used in a {room}, especially near any {animals}.\n\
      Send us your receipt and {amount} for shipping and handling.\
      We will send you another {product} that, in our tests,\
      is {percent}% less likely to have {verbed}.\n\
      Thank you for your support.\n\
      Sincerely,\n{spokesman}\n{job_title}"""

letter2=letter.format(**response)
print(letter2)