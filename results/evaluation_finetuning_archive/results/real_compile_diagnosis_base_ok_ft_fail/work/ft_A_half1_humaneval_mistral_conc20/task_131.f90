program digits_demo
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Call the function
  result = digits(n)

  ! Print output
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
      if (mod(digit, 2) == 1) then
        product = product * digit
        all_even = .false.
      end if
      temp = temp / 10
    end do

    if (all_even) then
      digits = 0
    else
      digits = product
    end if

  end function digits

end program digits_demo