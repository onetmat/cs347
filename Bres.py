

# Return a list of coordinates (col, row) that would be touched
# by a straight line from start to end.
def BresLine(start, end):
   (x0, y0) = start
   (x1, y1) = end

   dx = abs(x1-x0)
   dy = abs(y1-y0)

   sx = 0
   if x0 < x1:
      sx = 1
   else:
      sx = -1

   sy = 0
   if y0 < y1:
      sy = 1
   else:
      sy = -1

   err = dx-dy
   done = False

   pts = list()
   while not done:
      pts.append((x0, y0))
      if x0 == x1 and y0 == y1:
         done = True
         break
      e2 = 2*err
      if e2 > -1 * dy:
         err = err - dy
         x0 = x0 + sx
      if x0 == x1 and y0 == y1:
         pts.append((x0, y0))
         done = True
         break
      if e2 < dx:
         err = err + dx
         y0 = y0 + sy

   return pts
