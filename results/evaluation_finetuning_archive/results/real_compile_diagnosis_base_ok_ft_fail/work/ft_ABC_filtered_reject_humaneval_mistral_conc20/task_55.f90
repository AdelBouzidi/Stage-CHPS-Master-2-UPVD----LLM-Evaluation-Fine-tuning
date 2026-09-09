program fib_demo
  implicit none
  integer :: n, result
  integer, dimension(100) :: fib

  ! Initialize Fibonacci array
  fib(1) = 1
  fib(2) = 1
  do i = 3, 100
    fib(i) = fib(i-1) + fib(i-2)
  end do

  ! Read input
  read(*,*) n

  ! Output result
  print *, fib(n)
end program fib_demo