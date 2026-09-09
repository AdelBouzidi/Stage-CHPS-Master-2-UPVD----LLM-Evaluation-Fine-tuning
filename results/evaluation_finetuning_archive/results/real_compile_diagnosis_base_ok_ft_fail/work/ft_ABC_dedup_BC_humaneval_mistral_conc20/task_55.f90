program fib_demo
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Calculate Fibonacci number
  result = fib(n)

  ! Output result
  print *, result
contains

  integer function fib(n)
    implicit none
    integer, intent(in) :: n
    integer :: a, b, temp, i

    if (n <= 0) then
      fib = 0
    else if (n == 1) then
      fib = 1
    else
      a = 0
      b = 1
      do i = 2, n
        temp = a + b
        a = b
        b = temp
      end do
      fib = b
    end if
  end function fib

end program fib_demo