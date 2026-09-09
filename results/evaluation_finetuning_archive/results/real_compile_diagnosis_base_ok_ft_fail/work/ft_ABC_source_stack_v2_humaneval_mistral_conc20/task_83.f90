program starts_one_ends_demo
  implicit none
  integer :: n, result

  ! Hardcoded test case: n = 1
  n = 1
  result = starts_one_ends(n)
  print *, 'starts_one_ends(', n, ') =', result

contains

  integer function starts_one_ends(n)
    integer, intent(in) :: n
    integer :: i

    if (n == 1) then
       starts_one_ends = 1
    else
       starts_one_ends = 0
       do i = 10**(n-1), 10**n - 1
          if (i/10**(n-1) == 1 .or. mod(i,10) == 1) then
             starts_one_ends = starts_one_ends + 1
          end if
       end do
    end if
  end function starts_one_ends

end program starts_one_ends_demo