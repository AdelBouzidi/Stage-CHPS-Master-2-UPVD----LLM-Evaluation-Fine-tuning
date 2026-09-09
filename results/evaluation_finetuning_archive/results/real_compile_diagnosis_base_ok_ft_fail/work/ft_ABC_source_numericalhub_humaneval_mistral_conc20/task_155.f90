program even_odd_count
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b) :: num
  integer :: even_count, odd_count

  ! Read input
  read(*,*) num

  ! Count even and odd digits
  even_count = 0
  odd_count = 0
  do
    if (num == 0) exit
    if (mod(abs(num), 10) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
    num = num / 10
  end do

  ! Output result
  print *, even_count, odd_count

end program even_odd_count