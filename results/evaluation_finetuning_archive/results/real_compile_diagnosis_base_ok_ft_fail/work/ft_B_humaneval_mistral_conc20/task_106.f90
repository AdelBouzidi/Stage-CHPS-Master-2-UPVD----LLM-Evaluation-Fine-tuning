program factorial_sum
  implicit none
  integer :: n, i
  integer, allocatable :: result(:)
  
  read *, n
  
  allocate(result(n))
  
  do i = 1, n
    if (mod(i, 2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum_to(i)
    end if
  end do
  
  write (*, *) (result(i), i = 1, n)
  
  deallocate(result)
  
contains
  
  recursive function factorial(k) result(fact)
    integer, intent(in) :: k
    integer :: fact
    if (k <= 1) then
      fact = 1
    else
      fact = k * factorial(k - 1)
    end if
  end function factorial
  
  function sum_to(k) result(s)
    integer, intent(in) :: k
    integer :: s
    s = k * (k + 1) / 2
  end function sum_to
  
end program factorial_sum