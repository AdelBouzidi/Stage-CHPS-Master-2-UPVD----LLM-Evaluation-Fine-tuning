program truncate_number_demo
  implicit none
  real :: number, result

  ! Read input number from stdin
  read(*,*) number

  ! Calculate the decimal part
  result = number - int(number)

  ! Output the result
  print(*,*) result

end program truncate_number_demo