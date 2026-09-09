program fibonacci
  implicit none
  integer :: n, result

  read(*,*) n
  result = fib(n)
  print *, result

contains

  recursive integer function fib(i)
    if (i <= 1) then
      fib = i
    else
      fib = fib(i-1) + fib(i-2)
    end if
  end function fib

end program fibonacci