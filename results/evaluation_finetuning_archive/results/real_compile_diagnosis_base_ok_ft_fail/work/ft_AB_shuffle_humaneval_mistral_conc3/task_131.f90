program digits
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Calculate result
  result = digits(n)

  ! Output result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: temp, digit
    logical :: odd_found

    res = 1
    temp = n
    odd_found = .false.
    do while (temp > 0)
      digit = mod(temp, 10)
      if (mod(digit, 2) == 1) then
        res = res * digit
        odd_found = .true.
      end if
      temp = temp / 10
    end do

    if (.not. odd_found) then
      res = 0
    end if

  end function digits

end program digits