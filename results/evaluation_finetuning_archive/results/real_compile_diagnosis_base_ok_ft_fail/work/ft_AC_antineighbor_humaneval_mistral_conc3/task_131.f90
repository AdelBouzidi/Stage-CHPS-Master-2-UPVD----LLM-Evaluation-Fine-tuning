program digits
  implicit none
  integer :: n, result

  ! Read input
  read *, n

  ! Calculate result
  result = digits(n)

  ! Output result
  print *, result

contains

  integer function digits(n)
    integer, intent(in) :: n
    integer :: temp, digit, product
    logical :: all_even

    temp = abs(n)
    product = 1
    all_even = .true.

    do while (temp > 0)
      digit = mod(temp, 10)
      if (digit /= 0) then
        if (mod(digit, 2) /= 0) then
          product = product * digit
          all_even = .false.
        end if
      end if
      temp = temp / 10
    end do

    if (all_even) then
      digits = 0
    else
      digits = product
    end if
  end function digits

end program digits