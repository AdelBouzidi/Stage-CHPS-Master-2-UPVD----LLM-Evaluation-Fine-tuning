program digits
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Calculate the product of odd digits
  result = digits(n)

  ! Output the result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i, digit, temp

    res = 0
    temp = n
    do while (temp > 0)
      digit = mod(temp, 10)
      if (mod(digit, 2) == 1) then
        if (res == 0) then
          res = digit
        else
          res = res * digit
        end if
      end if
      temp = temp / 10
    end do

  end function digits

end program digits