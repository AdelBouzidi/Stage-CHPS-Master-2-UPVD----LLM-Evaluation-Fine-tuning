program fib
  implicit none
  integer :: n, result

  read(*,*) n
  result = fib(n)
  write(*,*) result

contains

  recursive function fib(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    if (n <= 1) then
      res = n
    else
      res = fib(n-1) + fib(n-2)
    end if
  end function fib

end program fib