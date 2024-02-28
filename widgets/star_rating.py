def show_star_rating(rating):
  rating = 11 - rating
  if rating < 1 or rating > 10:
    raise ValueError("Invalid rating value. Please provide a value between 1 and 10.")
  clip = "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)"
  star_html = "<div style='font-size: 20px; color: white;'>"
  for i in range(5):
    filled_portion = min(1, rating / 2)
    star_style = ""
    if filled_portion >= 1:
      star_style = ' style="color: gold;"' 
    elif filled_portion > 0:
      star_style = f' style="color: gold; clip-path: {clip};"'  
    star_html += f'<span{star_style}>&#9733;</span>'
    rating -= 2

  return star_html + "</div>"