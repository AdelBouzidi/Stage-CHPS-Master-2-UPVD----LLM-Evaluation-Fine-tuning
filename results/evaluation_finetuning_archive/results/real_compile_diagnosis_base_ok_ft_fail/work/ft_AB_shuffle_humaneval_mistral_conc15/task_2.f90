program truncate_number_demo
  implicit none
  real :: number, result

  ! Hardcoded input value
  number = 3.5

  result = truncate_number(number)

  print *, 'Truncated number:', result

contains

  function truncate_number(number) result(res)
    implicit none
    real, intent(in) :: number
    real :: res
    res = number - int(number)
  end function truncate_number

end program truncate_number_demo