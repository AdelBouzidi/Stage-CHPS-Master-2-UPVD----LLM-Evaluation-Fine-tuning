program vowels_count
  implicit none
  character(len=100) :: s
  integer :: count
  integer :: i
  character(len=1) :: ch

  read *, s
  count = 0
  do i = 1, len_trim(s)
    ch = s(i:i)
    select case (ichar(ch))
    case (ichar('a'), ichar('e'), ichar('i'), ichar('o'), ichar('u'))
      count = count + 1
    case (ichar('A'), ichar('E'), ichar('I'), ichar('O'), ichar('U'))
      count = count + 1
    case (ichar('y'), ichar('Y'))
      if (i == len_trim(s)) then
        count = count + 1
      end if
    end select
  end do

  print *, count

end program vowels_count