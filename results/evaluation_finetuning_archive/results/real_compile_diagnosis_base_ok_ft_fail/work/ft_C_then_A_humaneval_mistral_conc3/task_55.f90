program fib
  implicit none
  integer :: n, result
  read(*,*) n
  result = fib(n)
  print *, result
contains
  integer function fib(n)
    integer, intent(in) :: n
    if (n <= 0) then
      fib = 0
    else if (n == 1) then
      fib = 1
    else
      fib = fib(n-1) + fib(n-2)
    end if
  end function fib
end program fib