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
    result = [number + need, remaining - need]
  else
    result = [number + remaining, 0]
  end if

  ! Output result
  print(*,'(2I8)') result
end program rabbit