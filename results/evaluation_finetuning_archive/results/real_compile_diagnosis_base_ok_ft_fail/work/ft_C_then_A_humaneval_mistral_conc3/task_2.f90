program main
  implicit none
  real :: number
  real :: result

  ! Hardcoded input value
  number = 3.5

  result = truncate_number(number)

  print *, result
end program main