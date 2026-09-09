program rabbit
  implicit none
  integer :: number, need, remaining
  integer :: result(2)
  
  read(*,*) number
  read(*,*) need
  read(*,*) remaining
  
  if (remaining >= need) then
    result(1) = number + need
    result(2) = remaining - need
  else
    result(1) = number + remaining
    result(2) = 0
  end if
  
  print *, result(1), result(2)
  
end program rabbit