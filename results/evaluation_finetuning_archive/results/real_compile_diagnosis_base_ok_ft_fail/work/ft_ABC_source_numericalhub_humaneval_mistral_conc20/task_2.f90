program truncate_number_demo
  implicit none
  real :: number, result

  ! Read input from stdin
  read(*,*) number

  ! Call the function
  result = truncate_number(number)

  ! Write output to stdout
  print *, result

contains

  function truncate_number(number) result(res)
    implicit none
    real, intent(in) :: number
    real :: res
    integer :: int_part
    int_part = int(number)
    res = number - int_part
  end function truncate_number

end program truncate_number_demo