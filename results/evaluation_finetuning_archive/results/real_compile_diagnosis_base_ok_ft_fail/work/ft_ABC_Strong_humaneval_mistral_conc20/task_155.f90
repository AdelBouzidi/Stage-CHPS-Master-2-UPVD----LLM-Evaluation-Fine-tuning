program even_odd_count
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit
  integer :: i

  ! Read input from stdin
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert number to string and count even/odd digits
  do i = 1, len_trim(adjustl(adjustl(num)))
    digit = trim(adjustl(num))
    if (i == 1) then
      digit = trim(adjustl(num))
    end if
    if (i == 1) then
      digit = trim(adjustl(num))
    end if
  end do

  ! Count even and odd digits
  do i = 1, len_trim(adjustl(adjustl(num)))
    digit = trim(adjustl(num))
    if (i == 1) then
      digit = trim(adjustl(num))
    end if
    if (i == 1) then
      digit = trim(adjustl(num))
    end if
  end do

  ! Output results
  print *, even_count, odd_count

end program even_odd_count