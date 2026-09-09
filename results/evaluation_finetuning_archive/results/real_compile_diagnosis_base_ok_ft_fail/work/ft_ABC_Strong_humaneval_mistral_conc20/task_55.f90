program fib_demo
  implicit none
  integer :: n
  integer :: result

  ! Read input from stdin
  read(*,*) n

  ! Calculate Fibonacci number
  result = fib(n)

  ! Output result to stdout
  print *, result

contains

  recursive function fib(n) result(res)
    integer, intent(in) :: n
    integer :: res
    if (n <= 0) then
      res = 0
    else if (n == 1) then
      res = 1
    else
      res = fib(n-1) + fib(n-2)
    end if
  end function fib

end program fib_demo