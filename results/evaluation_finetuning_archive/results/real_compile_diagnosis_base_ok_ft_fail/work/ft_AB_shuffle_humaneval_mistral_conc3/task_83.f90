program starts_one_ends
  implicit none
  integer :: n
  integer :: result

  read(*,*) n
  result = starts_one_ends(n)
  print *, result

contains

  integer function starts_one_ends(n)
    integer, intent(in) :: n
    if (n == 1) then
      starts_one_ends = 1
    else
      starts_one_ends = 9 * 10**(n-1) + 8 * 10**(n-2)
    end if
  end function starts_one_ends

end program starts_one_ends