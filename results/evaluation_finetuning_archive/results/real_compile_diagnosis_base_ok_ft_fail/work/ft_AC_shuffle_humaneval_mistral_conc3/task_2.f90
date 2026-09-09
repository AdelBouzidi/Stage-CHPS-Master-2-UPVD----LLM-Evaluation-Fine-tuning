program truncate_number_demo
  implicit none
  real :: number
  real :: result

  ! Read input number from stdin
  read(*,*) number

  ! Call the function
  result = truncate_number(number)

  ! Print the result
  print *, result

contains

  function truncate_number(number) result(res)
    implicit none
    real, intent(in) :: number
    real :: res
    integer :: int_part
    res = number - int_part
  end function truncate_number

end program truncate_number_demo