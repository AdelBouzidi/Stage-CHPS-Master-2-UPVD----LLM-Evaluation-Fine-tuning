program rabbit
  implicit none
  integer :: number, need, remaining
  integer, dimension(2) :: result

  ! Read input
  read(*,*) number
  read(*,*) need
  read(*,*) remaining

  ! Calculate result
  if (remaining >= need) then
    result(1) = number + need
    result(2) = remaining - need
  else
    result(1) = number + remaining
    result(2) = 0
  end if

  ! Output result
  print(*,*) result(1), result(2)

end program rabbit