program main
  implicit none
  real :: number, result
  read *, number
  result = truncate_number(number)
  print *, result
contains
  function truncate_number(number) result
    real, intent(in) :: number
    real :: result
    result = number - int(number)
  end function truncate_number
end program main