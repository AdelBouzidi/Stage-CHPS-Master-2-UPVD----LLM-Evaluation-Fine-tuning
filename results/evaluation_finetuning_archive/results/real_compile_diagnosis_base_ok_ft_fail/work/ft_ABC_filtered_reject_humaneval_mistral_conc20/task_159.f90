program rabbit
  implicit none
  integer :: number, need, remaining
  integer, dimension(2) :: result
  
  ! Read input
  read(*,*) number
  read(*,*) need
  read(*,*) remaining
  
  ! Call the function
  result = eat(number, need, remaining)
  
  ! Print output
  print *, result(1), result(2)
  
contains

  function eat(number, need, remaining) result(res)
    implicit none
    integer, intent(in) :: number, need, remaining
    integer, dimension(2), intent(out) :: res
    
    if (remaining >= need) then
      res(1) = number + need
      res(2) = remaining - need
    else
      res(1) = number + remaining
      res(2) = 0
    end if
  end function eat

end program rabbit