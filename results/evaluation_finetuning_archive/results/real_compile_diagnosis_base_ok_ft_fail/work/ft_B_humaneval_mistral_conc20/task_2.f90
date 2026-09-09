program truncate_number
  implicit none
  real :: number, result
  
  read *, number
  result = number - int(number)
  write *, result
end program truncate_number