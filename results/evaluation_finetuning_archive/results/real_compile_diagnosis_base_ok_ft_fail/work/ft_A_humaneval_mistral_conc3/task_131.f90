program main
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Call the function
  result = digits(n)

  ! Output the result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: digit, product

    res = 0
    product = 1

    do while (n > 0)
      digit = mod(n, 10)
      if (mod(digit, 2) == 1) then
        product = product * digit
      else
        res = 0
        exit
      end if
      n = n / 10
    end do

    if (res == 0) then
      res = product
    end if

  end function digits

end program main